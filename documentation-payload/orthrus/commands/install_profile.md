+++
title = "install_profile"
chapter = false
weight = 100
hidden = false
+++

## Summary

Installs a profile on the device.
- Needs Admin: True  
- Version: 1  
- Author: @rookuu


### Arguments

#### file

File containing profile to install.

## Usage

``` 
install_profile
```

## MITRE ATT&CK Mapping

- T1072


## Detailed Summary

This is a very noisy and non-opsec safe command which can easily be instrumented.
```
install_profile <profile file>
```