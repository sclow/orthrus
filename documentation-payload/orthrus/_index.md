+++
title = "orthrus"
chapter = false
weight = 5
+++

![logo](/agents/orthrus/orthrus.svg?width=200px)
## Summary

Orthrus is a macOS agent that uses Apple's MDM to backdoor a device using a malicious profile. It effectively runs its own MDM server and allows the operator to interface with it using Mythic.

### Highlighted Agent Features
- No custom code introduced to the device.
- No beaconing behaviour, Orthrus will check in to Mythic when the operator tells it to using the `force_callback` command.
- SSL certificate of the MDM server trusted for code signing upon installation.
- Install PKG installers or Profiles.



### Important Notes
Orthrus uses Apple's Push Notification Service to send messages to the target device. For this reason, we need to configure APN push certificates. Some of the options for this can be found at [Understanding MDM Certificates](https://micromdm.io/blog/certificates/).

## Authors
- @rookuu
- @arubdesu

### Special Thanks to These Contributors
- @its_a_feature_
- @1njection
