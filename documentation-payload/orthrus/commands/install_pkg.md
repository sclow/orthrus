+++
title = "install_pkg"
chapter = false
weight = 100
hidden = false
+++

## Summary

Installs a pkg on the device. The pkg must be signed with the SSL cert of the mdm web server.
- Needs Admin: True  
- Version: 1  
- Author: @rookuu


### Arguments

#### file

File containing profile to install.

## Usage

``` 
install_pkg
```

## MITRE ATT&CK Mapping

- T1072 


## Detailed Summary

This is a very noisy and non-opsec safe command which can easily be instrumented.
```
install_pkg <signed_package_file>
```