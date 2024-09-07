## My own server unit.

### Contains:

1. Simple [xray](https://github.com/XTLS/Xray-core) implementation (named **xray**).
2. Assistant which (named **assistant**):
   1. Controls xray by grpc.
   2. Sends any alerts by TG bot.
3. Business card page for xray fallback (named **landing**).
4. **NGINX** http server for routing **1.** and **3.** (named **server**).
