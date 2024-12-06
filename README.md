<link
  href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
  rel="stylesheet"
/>

## <img src="./services/landing/src/assets/netku-dark.svg" alt="Netku logo" width="30px" style="position: relative;top: 6px;"/> My own server unit.

### Contains:

1. Simple [xray](https://github.com/XTLS/Xray-core) implementation (named **xray**).
2. Assistant which (named **assistant**):
   1. Controls xray by grpc.
   2. Sends any alerts by TG bot.
3. Business card page for xray fallback (named **landing**).
4. **NGINX** http server for routing **1.**, **2.** and **3.** (named **server**).
5. Web automation service for auto booking NSU washing machines (named **booking**).

---

```mermaid
---
title: Netku architecture
---
flowchart TD
    G@{shape: trap-t, label: "fa:fa-globe Gateway"}


    N(fa:fa-server Nginx)
    X(fa:fa-shield-halved Xray)

    NFallback@{ shape: braces, label: "xray fallback?"}
    Nhttp@{ shape: braces, label: "direct http?"}


    L(fa:fa-eye Landing)
    A(fa:fa-cloud Assistant)
    B(fa:fa-book Booking)
    P(fa:fa-database Postgres)
    M(fa:fa-database Mongo)

    G <-->|https| X
    G <--> |vless| X

    G -->|http| N
    X <--> |fallback| N


    N --> Nhttp
    N <--> NFallback

    Nhttp --> |https 301| G

    NFallback <--> |static| L
    NFallback <--> |bot webhook| A
    NFallback <--> |api| A

    A <-.-> |grpc|X
    A <-.-> |grpc|B

    A <--> P
    A <--> M
```

---

### Envs:

- You can open [envs](./.env.example) for looking environment variables off app.
