+++
title = "installed_application_list"
chapter = false
weight = 100
hidden = false
+++

## Summary

Retrieve a list of installed applications.
- Needs Admin: True  
- Version: 1  
- Author: @rookuu


### Arguments

#### N/A

No Arguments needed

## Usage

``` 
installed_application_list
```

## MITRE ATT&CK Mapping

- T1592.002


## Detailed Summary

This is a very noisy and non-opsec safe command since it is based on an embedded bash script which can easily be instrumented.
```
installed_application_list
```