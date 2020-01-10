import xml.etree.ElementTree as ET
import argparse


parser = argparse.ArgumentParser(description="Nmap IP/Port parser. This program need nmap xml output files.", \
    usage=' %(prog)s  [-h] -i INPUT [-o OUTPUT] \n\t\
    %(prog)s -i File_Name \n\t\
    %(prog)s -i File_Name1,File_Name2,File_Name3')
parser.add_argument("-i", "--input", type=str, required=True, help='File to parse')
parser.add_argument("-o", "--output", type=str, help='Output file')

args = parser.parse_args()

inputs=args.input.split(",")
for inputName in inputs:
    try:
        tree = ET.parse(inputName)
        root = tree.getroot()
        liste = {}

        for host in root.findall('host'):
            address=host.find('address')
            addr=address.get('addr')

            try:
                portsTag=host.find('ports')
                for portTek in portsTag.findall('port'):
                    portNum = portTek.get('portid')
                    if addr not in liste.keys():
                        liste[addr] = {'portNum': []}
                    liste[addr]['portNum'].append(portNum)

            except:
                print("No open ports found on ", addr, " address")

        if args.output:
            outputFile=args.output
        else:
            outputFile=inputName + ".csv"

        try:
            f = open(outputFile, "a")
            fileName = "----- Readed from " + inputName + " file -----,"
            f.write(fileName)

            for x in liste.keys():
                ipAdress = "\n" + x + ":"
                f.write(ipAdress)
                for i in liste[x]['portNum']:
                    portNumber = "," + i
                    f.write(portNumber)

            f.write("\n\n\n")
            f.close()

        except:
            print("Some output file problem")

    except:
        print(inputName, "file doesn't exist")