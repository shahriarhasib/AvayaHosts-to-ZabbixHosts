import csv
import yaml
from collections import OrderedDict

def represent_ordereddict(dumper, data):
    """Custom representer for OrderedDict to maintain key order in YAML"""
    return dumper.represent_dict(data.items())

yaml.add_representer(OrderedDict, represent_ordereddict)

def convert_csv_to_zabbix_yaml(csv_file, output_yaml):
    """
    Convert CSV file to Zabbix YAML format
    
    CSV Column mapping:
    - col1 (index 0): host identifier (e.g., 4036)
    - col3 (index 2): person name (e.g., Md. Saiful Islam)
    - col4 (index 3): IP address (e.g., 192.168.21.149)
    - col6 (index 5): device type (contains 'Avaya', '9608', 'J179', 'VPN', etc.)
    """
    
    hosts = []
    
    # Read CSV file with comma delimiter
    with open(csv_file, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file, delimiter=',')
        
        for row in csv_reader:
            # Skip blank lines or rows with insufficient data
            if not row or len(row) < 4 or not row[0].strip():
                continue
            
            # Extract data from CSV columns
            host_id = row[0].strip()
            host_name_part = row[2].strip() if len(row) > 2 else ''
            ip_address = row[3].strip() if len(row) > 3 else ''
            device_type = row[5].strip() if len(row) > 5 else ''
            
            # Skip if essential data is missing or invalid
            if not ip_address or not host_name_part:
                continue
            
            # Skip invalid IP addresses
            if ip_address in ['?', '0.0.0.0', '']:
                continue
            
            # Construct host name and host identifier
            host_name = f"{host_name_part}- {host_id}" if host_id else host_name_part
            # Create host identifier by replacing spaces with hyphens
            host_identifier = host_name.replace(' ', '-')
            
            # Determine if it's an Avaya device by checking for specific keywords
            avaya_keywords = ['avaya', '9608', 'j179', 'vpn', '9611', '9621', '9641']
            is_avaya = any(keyword in device_type.lower() for keyword in avaya_keywords)
            
            host_entry = OrderedDict()
            host_entry['host'] = host_identifier
            host_entry['name'] = host_name
            
            # Set templates based on device type
            if is_avaya:
                host_entry['templates'] = [{'name': 'ICMP Ping'}]
                host_entry['groups'] = [{'name': 'Avaya-Phones'}]
                # ICMP-based monitoring - simple interface
                host_entry['interfaces'] = [
                    OrderedDict([
                        ('ip', ip_address),
                        ('interface_ref', 'if1')
                    ])
                ]
            else:
                host_entry['templates'] = [{'name': 'Grandstream IP Phone'}]
                host_entry['groups'] = [
                    {'name': 'Grandstream-Phones'},
                    {'name': 'Non-Avaya-Phones'}
                ]
                # SNMP-based monitoring
                host_entry['interfaces'] = [
                    OrderedDict([
                        ('type', 'SNMP'),
                        ('ip', ip_address),
                        ('port', '161'),
                        ('details', {'community': '{$SNMP_COMMUNITY}'}),
                        ('interface_ref', 'if1')
                    ])
                ]
            
            host_entry['inventory_mode'] = 'DISABLED'
            
            hosts.append(host_entry)
    
    # Create the Zabbix export structure
    zabbix_export = OrderedDict([
        ('version', '7.0'),
        ('host_groups', [
            OrderedDict([
                ('uuid', '2c003def8ac347548313184aba503b4e'),
                ('name', 'Avaya-Phones')
            ]),
            OrderedDict([
                ('uuid', '10b0b449e93944efaee81257ffbcfb23'),
                ('name', 'Grandstream-Phones')
            ]),
            OrderedDict([
                ('uuid', '8070e73e3b6d4cae942dde73b38e898d'),
                ('name', 'Non-Avaya-Phones')
            ])
        ]),
        ('hosts', hosts)
    ])
    
    # Write to YAML file with custom formatting
    with open(output_yaml, 'w', encoding='utf-8') as yaml_file:
        # Custom YAML dumper for better formatting
        class CustomDumper(yaml.SafeDumper):
            pass
        
        def str_representer(dumper, data):
            if '\n' in data:
                return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
            return dumper.represent_scalar('tag:yaml.org,2002:str', data)
        
        CustomDumper.add_representer(OrderedDict, represent_ordereddict)
        CustomDumper.add_representer(str, str_representer)
        
        yaml.dump(
            {'zabbix_export': zabbix_export},
            yaml_file,
            Dumper=CustomDumper,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            width=1000,
            indent=2
        )
    
    print(f"✓ Conversion complete!")
    print(f"✓ Processed {len(hosts)} hosts")
    print(f"✓ Output saved to: {output_yaml}")
    
    # Print summary
    avaya_count = sum(1 for host in hosts if host['groups'][0]['name'] == 'Avaya-Phones')
    non_avaya_count = len(hosts) - avaya_count
    print(f"\nSummary:")
    print(f"  - Avaya phones: {avaya_count}")
    print(f"  - Non-Avaya phones: {non_avaya_count}")

if __name__ == "__main__":
    # Configuration
    csv_file = 'InceptaExt.csv'  # Change this to your CSV file path
    output_yaml = 'InceptaExt.yaml'
    
    try:
        convert_csv_to_zabbix_yaml(csv_file, output_yaml)
    except FileNotFoundError:
        print(f"✗ Error: CSV file '{csv_file}' not found!")
    except Exception as e:
        print(f"✗ Error during conversion: {str(e)}")
        import traceback
        traceback.print_exc()