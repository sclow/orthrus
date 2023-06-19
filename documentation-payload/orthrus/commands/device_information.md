+++
title = "device_information"
chapter = false
weight = 100
hidden = false
+++

## Summary

Returns a bunch of generic device information including hostname, os version and serial numbers.
- Needs Admin: True  
- Version: 1  
- Author: @rookuu


### Arguments

#### N/A

No Arguments needed

## Usage

``` 
device_information
```

## MITRE ATT&CK Mapping

- T1592.001


## Detailed Summary

This is a very noisy and non-opsec safe command since it is based on an embedded bash script which can easily be instrumented.
```
device_information
```