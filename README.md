<link
  href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
  rel="stylesheet"
/>

## <img src="./clients/landing/src/assets/icons/netku-dark.svg" alt="Netku logo" width="30px" style="position: relative;top: 6px;"/> My own server unit.

```mermaid
---
title: Architecture
---
flowchart TD
    G(fa:fa-dungeon Gate)
    T(fa:fa-message Telegram)

    subgraph Proxy [Proxy graph]
      X(fa:fa-shield-halved Xray)
      P(fa:fa-user-tie Proxy)
      XN(fa:fa-server Nginx)
      L(fa:fa-eye Landing)
      Re(fa:fa-database Redis)
    end
    G <--> |vless, https| P & X
    P --> |grpc| X
    X <--> |fallback| XN
    XN <--> |static| L

    Ra(fa:fa-message RabbitMQ)

    X <--> Re
    P <--> Re
    P <----> Ra

    As(fa:fa-cloud Assistant)
    U(fa:fa-user User)
    Au(fa:fa-lock Auth)
    G1(fa:fa-dungeon Gate)

    T <--> As <--> U & Ra
    U <--> Au <--> Ra
    Au & U <--> |API| G1

```

---

### Envs:

Each service has own env variables.
You might check them in corresponding folders.
