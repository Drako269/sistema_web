import subprocess

def block_website(domain):
    print(f"Bloqueando dominio: {domain}")
    with open('C:\\path_to_squid_config\\squid.conf', 'a') as f:
        f.write(f"\nacl blocked dstdomain {domain}\nhttp_access deny blocked\n")
    subprocess.run(["net", "stop", "squid"], shell=True)  # Detener Squid
    subprocess.run(["net", "start", "squid"], shell=True)  # Iniciar Squid

def update_squid_config(blocked_sites):
    with open('/etc/squid/squid.conf', 'a') as f:
        for site in blocked_sites:
            f.write(f"acl blocked dstdomain {site}\n")
            f.write("http_access deny blocked\n")
    
    subprocess.run(["sudo", "service", "squid", "restart"])