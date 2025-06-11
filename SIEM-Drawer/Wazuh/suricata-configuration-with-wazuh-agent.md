# Setting up Suricata IDS/IPS on A Debian Based Distro

## Adding Suricata Repository

```
sudo add-apt-repository ppa:oisf/suricata-stable
sudo apt-get update
sudo apt-get install suricata -y
```

## Getting and Adding Emerging Threats Detection Rules

```
cd /tmp/ && curl -LO https://rules.emergingthreats.net/open/suricata-6.0.8/emerging.rules.tar.gz
sudo tar -xvzf emerging.rules.tar.gz && sudo mkdir /etc/suricata/rules && sudo mv rules/*.rules /etc/suricata/rules/
sudo chmod 640 /etc/suricata/rules/*.rules
```

Modify Suricata settings in the /etc/suricata/suricata.yaml file and set the following variables:

```
HOME_NET: "<UBUNTU_IP>"
EXTERNAL_NET: "any"

default-rule-path: /etc/suricata/rules
rule-files:
- "*.rules"

# Global stats configuration
stats:
enabled: yes

# Linux high speed capture support
af-packet:
  - interface: <interface>
```

Restart the Suricata service

```
sudo systemctl restart suricata
```

## Using Suricata with Wazuh Agent

Add the following configuration to the /var/ossec/etc/ossec.conf file of the Wazuh agent.

This allows the Wazuh agent to read Suricata log files:

```
<ossec_config>
  <localfile>
    <log_format>json</log_format>
    <location>/var/log/suricata/eve.json</location>
  </localfile>
</ossec_config>
```

Restart the Wazuh Agent

```
sudo systemctl restart wazuh-agent
```

**And you're good to go:D**
