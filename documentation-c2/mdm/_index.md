+++
title = "mdm"
chapter = false
weight = 5
+++

## Overview
This C2 profile consists of HTTP requests from an agent to the C2 profile container, where messages are then forwarded to Mythic's API. The C2 Profile container acts as a proxy between agents and the Mythic server itself.

The Profile is not proxy aware by default - this is a component left as an exercise for the individual agents. 
### C2 Workflow
#### New Agent

{{<mermaid>}}
sequenceDiagram
    participant E as Mythic Operator
    participant M as Mythic
    participant D as MDM
    E ->>+ M: Operator Requests New Orthrus Payload
    M ->>+ D: Mythic Attempts to enroll new device 
    D -->>- M: Mythic Patches response with Orthrus configuration
    M -->>- E: Operator downloads weaponised .mobileconfig
{{< /mermaid >}}    
Legend:

- Solid line is a new connection
- Dotted line is a message within that connection

#### Payload Delivery

{{<mermaid>}}
sequenceDiagram
    participant E as Mythic Operator
    participant V as Delivery Vector
    participant C as Victim Mac Client
    participant D as MDM
    participant M as Mythic Server
    E ->>+ V: Operator uploads .mobileconfig to Delivery Vector
    V ->>+ C: Delivery Vector transfers .mobileconfig to Victim
    C -->>- C: Victim install's .mobileconfig registering new MDM
    C ->>+ D: Victim enrolls to MicroMDM instance
    D ->>+ M: MicroMDM calls Mythic Webhook to register new callback
{{< /mermaid >}}    
Legend:

- Solid line is a new connection
- Dotted line is a message within that connection


#### Task Execution
{{<mermaid>}}
sequenceDiagram
    participant E as Mythic Operator
    participant M as Mythic Server
    participant A as Apple Push Notification
    participant C as Victim Mac Client
    participant D as MDM
    
    E ->>+ M: Operator Requests New Task
    M ->>+ A: Mythic Creates a new Apple Push Notification with task
    A ->>+ C: Victim receives new push notification
    C ->>+ D: Victim requests task from MDM
    D -->>- C: reply with tasking
    C ->>+ D: Victim provides results of a task
    D -->>- M: MDM Pushes task results to Mythic Server
{{< /mermaid >}}
Legend:

- Solid line is a new connection
- Dotted line is a message within that connection

## Configuration Options
The profile reads a `config.json` file for a set of instances of `Sanic` webservers to stand up (`8035` by default) and redirects the content.

```JSON
{
  "webhook_port": 8035,
  "mdm_host": "172.17.2.81",
  "mythic_mdm_bind_address": 12345,
  "tls_cert": "TLS CERT GOES HERE",
  "tls_key": "TLS KEY GOES HERE",
  "apn_cert": "APN CERT GOES HERE",
  "apn_key": "APN KEY GOES HERE",
  "debug": true
}

```

You can specify the headers that the profile will set on Server responses. If there's an error, the server will return a `404` message based on `server_error_handler` handler in `C2_Profiles/mdm/c2_code/server`.

This C2 service makes use of certificates that are generated as part of the MDM onboarding process. 
You should get a notification when the server starts with information about the configuration:

```
Started with pid: 21...
Output:Opening config and starting mdm...
Debugging statements are enabled. This gives more context, but might be a performance hit
Writing stanza 'tls_cert' to file '/Mythic/mdm/certs/mdm.crt'
main_config[tls_cert] appears to contain valid Base64 will write to file.
Writing stanza 'tls_key' to file '/Mythic/mdm/certs/mdm.key'
main_config[tls_key] appears to contain valid Base64 will write to file.
MDM SSL - Currently unconfigured:
No APN Certificate key present; you need to get one for this to work.
component=main msg=started
ts="2023/06/19 12:01:55" msg="push: waiting for push certificate before enabling APNS service provider"
level=debug component=depsync msg="loaded DEP config" cursor=
level=info component=depsync msg="waiting for DEP token to be added before starting sync"
level=info msg="serving HTTPS using provided certificates" addr=:https
[2023-06-19 12:01:55 +0000] [23] [DEBUG] 

                 Sanic
         Build Fast. Run Fast.

```



### Profile Options

#### webhook_port
The TCP port on which the webhook will exist

#### mythic_mdm_bind_address
The TCP port for the HTTPS portion of the MicroMDM instance to bind too. 
You will either need to reference that address in the callback, or to set up a reverse proxy to serve it. 

#### mdm_host
The publicly accessible IP address or hostname for the MDM Host. 

#### tls_cert
The TLS Certificate for the MDM in Base64 format.

#### tls_key
The TLS Private Key for the MDM in Base64 format

#### apn_cert
The Apple Push Notification Service (APN) certificate in Base64 format.

#### apn_key
The Apple Push Notification Service (APN) private key in Base64 format.

#### debug
Boolean to enable or disable debugging within the MDM server code. 

A note about debugging:
- With `debug` set to `true`, you'll be able to `view stdout/stderr` from within the UI for the container, but it's not recommended to always have this on (especially if you start using something like SOCKS). There can be a lot of traffic and a lot of debugging information captured here which can be both a performance and memory bottleneck depending on your environment and operational timelines.
- It's recommended to have it on initially to help troubleshoot payload connectivity and configuration issues, but then to set it to `false` for actual operations

## OPSEC

This profile doesn't do any randomization of network components outside of allowing operators to specify internals/jitter. 

Expect the MicroMDM instance to be a finger print and be willing to be burned. 

## Development

All of the code for the server is Python3 using `Sanic` and located in `C2_Profiles/mdm/c2_code/server`. 
