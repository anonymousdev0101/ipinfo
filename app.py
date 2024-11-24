import streamlit as st
import whois
import socket
import requests
from ipwhois import IPWhois
from bs4 import BeautifulSoup
import dns.resolver

# Function to fetch WHOIS info for domain
# Function to fetch WHOIS info for domain
def get_whois_info(domain):
    try:
        w = whois.whois(domain)  # This will fetch the WHOIS info
        return w
    except Exception as e:
        return f"Error: {e}"

# Function to get basic info about the IP address
def get_ip_info(ip_address):
    try:
        ip_info = IPWhois(ip_address).lookup_rdap()
        return ip_info
    except Exception as e:
        return f"Error: {e}"

# Function to get DNS records for a domain
def get_dns_info(domain):
    try:
        result = {}
        result['A'] = dns.resolver.resolve(domain, 'A')
        result['MX'] = dns.resolver.resolve(domain, 'MX')
        result['TXT'] = dns.resolver.resolve(domain, 'TXT')
        return result
    except Exception as e:
        return f"Error: {e}"

# Function to get the webpage title using requests and BeautifulSoup
def get_page_title(domain):
    try:
        response = requests.get(f'http://{domain}')
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No title found"
        return title
    except Exception as e:
        return f"Error: {e}"

# Streamlit app
st.title("IP & Domain Information Finder")

# Input field for user to enter domain or IP address
input_type = st.selectbox("Select Input Type", ["Domain", "IP Address"])
user_input = st.text_input(f"Enter {input_type}")

if user_input:
    if input_type == "Domain":
        st.subheader(f"WHOIS Info for {user_input}")
        whois_info = get_whois_info(user_input)
        st.write(whois_info)

        st.subheader(f"DNS Records for {user_input}")
        dns_info = get_dns_info(user_input)
        st.write(dns_info)

        st.subheader(f"Webpage Title for {user_input}")
        title = get_page_title(user_input)
        st.write(title)

    elif input_type == "IP Address":
        st.subheader(f"IP Info for {user_input}")
        ip_info = get_ip_info(user_input)
        st.write(ip_info)

