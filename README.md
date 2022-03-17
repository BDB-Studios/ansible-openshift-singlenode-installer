# ansible-openshift-singlenode-installer

Ansible Role to Create a RHEL based sno installer Iso on the Bootstrap node

### Example playbook
```yaml
- name: Create Single Node Boot Iso
  hosts: localhost
  become: true
  vars:
    install_config:
      domain_name: "openshift.local"
      cluster_name: "single-node"
      network:
        cluster_network:
          cidr: "10.128.0.0/14"
          prefix: 23
        service_network:
          - "172.30.0.0/16"
      installation_disk: "/dev/sda"
      openshift_pull_secret: ""
      pub_key_path: ""
      pub_key_contents: ""
      openshift_pull_secret_path: "/tmp/pull_secret_pretty.json"

  roles:
    - ansible-openshift-singlenode-installer
```
