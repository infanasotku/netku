## <img src="https://raw.githubusercontent.com/infanasotku/netku/master/services/landing/public/img/netku.svg" alt="Netku logo" width="22px" style="position: relative;top: 4px;"/> My own server unit.

### Contains:

1. Simple [xray](https://github.com/XTLS/Xray-core) implementation (named **xray**).
2. Assistant which (named **assistant**):
   1. Controls xray by grpc.
   2. Sends any alerts by TG bot.
3. Business card page for xray fallback (named **landing**).
4. **NGINX** http server for routing **1.**, **2.** and **3.** (named **server**).
5. Web automation service for auto booking NSU washing machines (named **booking**).

---

### Assitants envs:

##### General

- `HOST`: Adress for serving.
- `PORT`: PORT for serving.
- `DOMAIN`: Domain name
- `SSL_CERTFILE`: Path to ssl cert file.
- `SSL_KEYFILE`: Path to ssl key file.

##### Xray

- `XRAY_RESTART_MINUTES`: Minutes between restarting xray.
- `XRAY_PORT`: Port for communicated with xray service.
- `XRAY_HOST`: Adress for communicated with xray service.
- `XRAY_RECONNECTION_RETRIES`: Count of retries to reconnect to xray.
- `XRAY_RECONNECTION_DELAY`: Delay in seconds between reconnection retries.
- `BOT_TOKEN`: Bot token from bot father.
- `TELEGRAM_TOKEN`: Telegram secret.
- `BOT_WEBHOOK_URL`: Webhook url for telegram.

##### DB

- `POSTGRES_PASSWORD`: DB password.
- `POSTGRES_USER`: DB user.
- `POSTGRES_HOST`: DB host.
- `POSTGRES_PORT`: DB port.
- `POSTGRES_DB_NAME`: DB name.

### Xray envs:

- `XRAY_PORT`: PORT for serving.
- `XRAY_FALLBACK`: Address for fallback (with port if need).
- `XRAY_CONFIG_DIR`: Folder where xray take config.
- `XRAY_LOG_DIR`: Folder where xray put logs.
- `SSL_CERTFILE`: Path to ssl cert file.
- `SSL_KEYFILE`: Path to ssl key file.

### Server envs:

- `DOMAIN`: Server domain name.
