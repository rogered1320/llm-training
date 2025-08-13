**Important:** Before deploying or testing locally, update the value of `chatUrl` in `main.js` to point to your API Gateway endpoint.

For local development, use:

```js
const chatUrl = "http://localhost:3000/chat";
```

For deployment, use your API Gateway URL, for example:

```js
const chatUrl = "https://api.execute-api.us-west-2.amazonaws.com/dev/chat";
```

## Frontend Application

This is the frontend for the chat application. It is a simple web interface built with HTML, CSS, and JavaScript.

### Deployment

The frontend is deployed to an AWS S3 bucket as a static website. To deploy or update the frontend, upload the contents of this directory (including `index.html`, `main.js`, and `style.css`) to your S3 bucket configured for static website hosting.

#### Steps to Deploy

1. Build or update your static files as needed.
2. Log in to your AWS account and navigate to the S3 service.
3. Select your S3 bucket configured for static website hosting.
4. Upload or replace the files (`index.html`, `main.js`, `style.css`, etc.) in the bucket.
5. Make sure the files are publicly accessible if you want the site to be available to everyone.
6. Access your frontend via the S3 website endpoint URL provided by AWS.

### Usage

Open the website in your browser using the S3 bucket's website endpoint. The frontend will connect to the backend API as configured in `main.js`.

### File Overview

- `index.html`: Main HTML file for the web interface.
- `main.js`: JavaScript logic for interacting with the backend API.
- `style.css`: Styles for the frontend UI.

---
For any issues or questions, please contact the project maintainer.
