import requests
from urllib3.exceptions import InsecureRequestWarning
import json
from optparse import OptionParser
import sys
try:
    from bs4 import BeautifulSoup
except:
    print("Unable to import Python module BeautifulSoup. Please run: pip3 install BeautifulSoup4")
    sys.exit()

if __name__ == "__main__":

    optp = OptionParser()
    optp.add_option("-u", "--username",       dest="username",       help="Ambari Admin Username")
    optp.add_option("-p", "--password",       dest="password",       help="Ambari Admin Password")
    optp.add_option("-o", "--outputfilename", dest="outputfilename", help="Output filename to save the CSV output")
    optp.add_option("-a", "--serverurl",      dest="serverurl",      help="URL of Ambari/Cloudera Manager, including port")

    opts, args = optp.parse_args()

    username = ''
    password = ''
    serverurl = ''

    exit = False
    if opts.username:
       username = opts.username
    else:
       print("Please set the Ambari/Cloudera Manager admin username: -u")
       exit = True
        
    if opts.password:
        password = opts.password
    else:
       print("Please set the Ambari/Cloudera Manager admin password: -p")
       exit = True

    if opts.serverurl:
        serverurl = opts.serverurl
    else:
       print("Please set the Ambari/Cloudera Manager HTTP URL: -a")
       exit = True

    if exit: 
        print("\nExample Usage (Ambari):           python3 query_ambari.py -c admin -p 2a613dc12d -a http://ambari-prod.example.com:8080")
        print("Example Usage (Cloudera Manager): python3 query_ambari.py -c admin -p 2a613dc12d -a http://cloudera-prod-manager.example.com:7180\n")
        sys.exit()

    
# Disable SSL warnings
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Workout if we are using Ambari or Cloudera Manger
# Let's try Cloudera Manager first, it should respond to: /api/v1/cm/version
using_cm=False
using_ambari=False
try:
    print("\nTesting for Cloudera Manager API: ")
    response = requests.get(serverurl + '/api/v1/cm/version', auth=requests.auth.HTTPBasicAuth(username, password), verify=False)
    jsn = json.loads(response.text) 
    if jsn['version']:
        using_cm=True
        print("We are using Cloudera Manager")
except:
    print("We are not using Cloudera Manager")
    None


# If we are not using Cloudera Manager, let's try Ambari
if not using_cm:
    try:
        print("\nTesting for Ambari API: ")
        response = requests.get(serverurl + '/api/v1/clusters/', 
                                auth=requests.auth.HTTPBasicAuth(username, password), verify=False) 
        jsn = json.loads(response.text)
        if jsn['items']:
            using_ambari=True
            clustername = str(jsn['items'][0]['Clusters']['cluster_name'])
            print("We are using Ambari: " + clustername)
    except:
        print("We are not using Ambari")
        None

if using_cm or using_ambari: 
    print("\nGenerating CSV (please wait, this might take a while):\n")
    None
else:
    print("\n\nUnable to determine if you're using either Cloudera Manager or Ambari Server. Stopping now...\n")
    sys.exit()


###################
# Print CSV Headers
outputstring = 'ClusterName,Version,Hostname,OSType,CPUCount,TotalMemBytes,TotalMemMB,DiskCount,TotalDiskStorage,TotalDiskStorageMB,HostComponents' + "\n"
 

if using_cm:
    response_cookies = response.cookies
    response = requests.get(serverurl + '/cmf/hardware/hosts/hostsOverview.json', 
                            auth=requests.auth.HTTPBasicAuth(username, password), verify=False, cookies=response_cookies) 
    jsn = json.loads(response.text)

    for x in jsn['hosts']:
        serverid = x['id']

        # Do another special URL call to find the OS Distribution
        response_host = requests.get(serverurl + '/cmf/hardware/hosts/' + str(serverid) + '/status', 
                                     auth=requests.auth.HTTPBasicAuth(username, password), verify=False, cookies=response_cookies)

        # Parse the HTML output to find the Distribution row for the column value
        soup = BeautifulSoup(response_host.text, 'html.parser')
        table = soup.find('table')
 
        distribution = False
        os = ''
        try:
            rows = table.findChildren(['th', 'tr'])
            for row in rows:
                cells = row.findChildren('td')
                for cell in cells:
                    value = cell.string
                    if distribution:
                        os = str(value).strip()
                        distribution = False
                    if str(value).strip() == 'Distribution':
                        distribution = True
        except:
            None

        roles = ''
        count = 0
        # Build a list of roles this server has
        for r in jsn['roleFilters']:
            if serverid in jsn['roleFilters'][r]:
                count += 1
                if count > 1:
                    roles += ';'
                roles += r

        outputstring += str(x['clusterName']) +','
        outputstring += str(x['cdhVersion']) +','
        outputstring += str(x['hostName']) +','
        outputstring += str(os) +','
        outputstring += str(x['numCores']) +','
        outputstring += str(x['physicalMemoryTotal']) +','
        outputstring += str(int(round(int(x['physicalMemoryTotal'])/1024,0))) +','
        outputstring += str("NA") +','
        outputstring += str(x['diskTotal']) +','
        outputstring += str(int(round(int(x['diskTotal'])/1024,0))) +','
        outputstring += str(roles) + "\n"
        
       
        
if using_ambari:
    response = requests.get(serverurl + '/api/v1/clusters/' + clustername + '/hosts?fields=*', 
                            auth=requests.auth.HTTPBasicAuth(username, password), verify=False) 
    jsn = json.loads(response.text)

    for x in jsn['items']:
    
        disk_count = 0
        total_disk_storage = 0
        for d in x['Hosts']['disk_info']:
            disk_count += 1
            total_disk_storage += int(d['size'])

        components = ''
        count = 0 
        for c in x['host_components']:
            count += 1
            if count > 1:
                components += ';'
            components += c['HostRoles']['component_name']
    
        stacks = ''
        count = 0
        for s in x['stack_versions']:
            count += 1
            if count > 1:
                stacks += ';'
            stacks = s['HostStackVersions']['stack'] + ' ' + s['HostStackVersions']['version']
        
        outputstring += str(x['Hosts']['cluster_name']) +','
        outputstring += str(stacks) +','
        outputstring += str(x['Hosts']['host_name']) +','
        outputstring += str(x['Hosts']['os_type']) +','
        outputstring += str(x['Hosts']['cpu_count']) +','
        outputstring += str(x['Hosts']['total_mem']) +','
        outputstring += str(int(round(int(x['Hosts']['total_mem'])/1024,0))) +','
        outputstring += str(disk_count) +','
        outputstring += str(total_disk_storage) +','
        outputstring += str(int(round(int(total_disk_storage)/1024,0))) +','
        outputstring += str(components) + "\n"

# Check if we need to write to console or file output
if opts.outputfilename:
    print("Redirecting the output to CSV file: " + str(opts.outputfilename))
    try:
        fh = open(opts.outputfilename,'w')
        fh.write(outputstring)
        fh.close()
        print("File saved.\n")
    except:
        print("Unable to save output to file, printing to screen instead:\n")
        print(str(outputstring))        
else:
   print(str(outputstring))

