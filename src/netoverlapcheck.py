#!/usr/bin/env python3

import ipaddress
import subprocess
import json
import sys
import argparse

def run_gcloud_command(command):
    """Run a gcloud command and return the output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running gcloud command: {command}")
        print(f"Error: {e.stderr}")
        return None

def get_project_subnets(project_id, network_name=None):
    """Get all subnet CIDR ranges for a project, optionally filtered by network"""
    if network_name:
        command = f"gcloud compute networks subnets list --project={project_id} --filter='network:{network_name}' --format='value(ipCidrRange)'"
    else:
        command = f"gcloud compute networks subnets list --project={project_id} --format='value(ipCidrRange)'"
    
    output = run_gcloud_command(command)
    if output:
        return [cidr.strip() for cidr in output.split('\n') if cidr.strip()]
    return []

def get_project_networks(project_id):
    """Get list of VPC networks in a project"""
    command = f"gcloud compute networks list --project={project_id} --format='value(name)'"
    output = run_gcloud_command(command)
    if output:
        return [net.strip() for net in output.split('\n') if net.strip()]
    return []

def get_existing_peerings(project_id, network_name=None):
    """Get existing peering connections"""
    if network_name:
        command = f"gcloud compute networks peerings list --project={project_id} --filter='network:{network_name}' --format='table(name,network,peerNetwork)'"
    else:
        command = f"gcloud compute networks peerings list --project={project_id} --format='table(name,network,peerNetwork)'"
    
    output = run_gcloud_command(command)
    return output if output else "No existing peerings found"

def check_network_overlaps(networks_a, networks_b):
    """
    Check if any networks in list A overlap with any networks in list B
    
    Args:
        networks_a (list): List of network CIDR strings
        networks_b (list): List of network CIDR strings
    
    Returns:
        tuple: (bool, list) - (has_overlaps, list_of_overlap_details)
    """
    if not networks_a or not networks_b:
        return False, []
    
    overlaps = []
    
    # Convert string CIDRs to IPv4Network objects
    try:
        nets_a = [ipaddress.IPv4Network(net, strict=False) for net in networks_a]
        nets_b = [ipaddress.IPv4Network(net, strict=False) for net in networks_b]
    except ValueError as e:
        print(f"Error parsing network: {e}")
        return False, []
    
    # Check each network in A against each network in B
    for net_a in nets_a:
        for net_b in nets_b:
            if net_a.overlaps(net_b):
                overlaps.append({
                    'network_a': str(net_a),
                    'network_b': str(net_b),
                    'overlap_type': get_overlap_type(net_a, net_b)
                })
    
    return len(overlaps) > 0, overlaps

def get_overlap_type(net_a, net_b):
    """Determine the type of overlap between two networks"""
    if net_a == net_b:
        return "identical"
    elif net_a.subnet_of(net_b):
        return f"{net_a} is subnet of {net_b}"
    elif net_b.subnet_of(net_a):
        return f"{net_b} is subnet of {net_a}"
    else:
        return "partial overlap"

def check_peering_eligibility(project_a, project_b, network_a=None, network_b=None):
    """Main function to check VPC peering eligibility between two projects"""
    
    print("=" * 60)
    print("GCP VPC PEERING ELIGIBILITY CHECKER")
    print("=" * 60)
    print(f"Project A: {project_a}")
    print(f"Project B: {project_b}")
    if network_a:
        print(f"Network A: {network_a}")
    if network_b:
        print(f"Network B: {network_b}")
    print()
    
    # Get subnet information
    print("Fetching subnet information...")
    subnets_a = get_project_subnets(project_a, network_a)
    subnets_b = get_project_subnets(project_b, network_b)
    
    if not subnets_a:
        print(f"❌ No subnets found in Project A ({project_a})")
        return False
    
    if not subnets_b:
        print(f"❌ No subnets found in Project B ({project_b})")
        return False
    
    print(f"Project A subnets: {subnets_a}")
    print(f"Project B subnets: {subnets_b}")
    print()
    
    # Check for overlaps
    print("Checking for IP range overlaps...")
    has_overlaps, overlap_details = check_network_overlaps(subnets_a, subnets_b)
    
    if has_overlaps:
        print("❌ OVERLAP DETECTED - VPC Peering NOT possible!")
        print("\nOverlapping networks:")
        for overlap in overlap_details:
            print(f"  • {overlap['network_a']} ↔ {overlap['network_b']}")
            print(f"    Type: {overlap['overlap_type']}")
        eligible = False
    else:
        print("✅ NO IP OVERLAPS - VPC Peering is possible!")
        eligible = True
    
    print(f"\nTotal overlaps found: {len(overlap_details)}")
    print()
    
    # Show existing peerings
    print("Existing peering connections:")
    print("Project A:")
    peerings_a = get_existing_peerings(project_a, network_a)
    print(peerings_a)
    print("\nProject B:")
    peerings_b = get_existing_peerings(project_b, network_b)
    print(peerings_b)
    
    return eligible

def main():
    parser = argparse.ArgumentParser(description='Check VPC peering eligibility between two GCP projects')
    parser.add_argument('project_a', help='First GCP project ID')
    parser.add_argument('project_b', help='Second GCP project ID')
    parser.add_argument('--network-a', help='Specific network name in project A (optional)')
    parser.add_argument('--network-b', help='Specific network name in project B (optional)')
    
    args = parser.parse_args()
    
    # Check if gcloud is available
    if not run_gcloud_command("gcloud --version"):
        print("Error: gcloud CLI not found. Please install and configure gcloud.")
        sys.exit(1)
    
    try:
        eligible = check_peering_eligibility(
            args.project_a, 
            args.project_b, 
            args.network_a, 
            args.network_b
        )
        
        print("\n" + "=" * 60)
        if eligible:
            print("✅ RESULT: Projects are eligible for VPC peering!")
        else:
            print("❌ RESULT: Projects are NOT eligible for VPC peering!")
        print("=" * 60)
        
        sys.exit(0 if eligible else 1)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()