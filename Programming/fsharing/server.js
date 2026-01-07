const http = require('http')

const loginHTML = `
<html>
<body>
	<h2>Login page</h2>
	<form type="application/x-www-form-urlencoded" method="POST" action="/login">
		<input name="username" placeholder="Login" />
		<br/>
		<input type="password" name="password" placeholder="Password" />
		<button>
			Login
		</button>
	</form>
</body>	
</html>
`

function renderIndexHTML(name) {
	return `
		<html>
		<body>
			<h2>Home page</h2>
			<br/>
			<h3>Hi ${name}</h3>
			<form action='/upload' method='POST' enctype='multipart/form-data'>
				<input type="file" name="file" >
				<button>
					Upload
				</button>
			</form>

		</body>	
		</html>
		`
}
function parse(data, splitter) {
	const keyValuePairs = data.split(splitter); 
	const body = {}

	for(let i = 0; i < keyValuePairs.length; i++) {
		const pair = keyValuePairs[i].split("=");
		if(pair.length === 1) {
			body[pair[0].trim()] = true;
		} else {
			const key = pair[0].trim();
			const value = pair[1].trim();
			body[key] = value;
		}
	}
	return body;
}

const users = [
	{ id: 1, fullName: "Saro Amirkhanyan", username: "saro", password: "saro" },
	{ id: 2,  fullName: "Michael Hovhannisyan", username: "miqo", password: "saro" },
];

const sessions = {};

function getSession(req) {
	const cookies = parse(req.headers.cookie, ';');
	return sessions[cookies.sessionId];
}

function randomToken() {
	return Math.random().toString().slice(2)
}

function handleLogin(req, res) {
	const session = getSession(req)

	if(session) {
		return redirect(res, '/');
	}

	if(req.method === "GET") {
		res.end(loginHTML);
		return;
	}
	if (req.method === "POST") {
		const chunks = [];
		req.on("data", function (chunk) {
			chunks.push(chunk);
		});

		function processBody() {
			const bodyString = Buffer.concat(chunks).toString("utf-8");
			const body = parse(bodyString, "&");

			if(!body.username) {
				res.end("username is required");
				return;
			}

			if(!body.password) {
				res.end("password is required");
				return;
			}

			let user;

			for(let i = 0; i < users.length; i++) {
				if(users[i].username === body.username &&
					users[i].password === body.password) {
					user = users[i];	
					break;
				}

			}

			if(user) {
				const session = {
					id: randomToken(),
					userId: user.id,
				};
				sessions[session.id] = session;

				res.writeHead(302, {
					'Location': '/',
					'Set-Cookie': `sessionId=${session.id}; HttpOnly; Max-Age=3600;Path=/`,
				});
				res.end();
				return;
			} else {
				res.end(`username or password is incorrect`);
			}
		}

		req.on("end", processBody);
		return;
	} 
	res.end(`Route not found for ${req.method} ${req.url}`);

}

function handleIndex(req, res) {
	const session = getSession(req)

	if(!session) {
		redirect(res, '/login');
		return;
	}

	let user;

	for(let i = 0; i < users.length; i++) {
		if(users[i].id === session.userId) {
			user = users[i];	
			break;
		}

	}

	res.end(renderIndexHTML(user.fullName));
}

function redirect(res, path) {
	res.writeHead(302, {
		'Location': path,
	});
	res.end();
}


function handleUpload(req, res) {
	const session = getSession(req)
	if(!session) {
		return redirect(res, '/login')
	}

	const chunks = [];
	req.on("data", function (chunk) {
		chunks.push(chunk);
	});
	function parseFile(chunk) {
		const parsedContentType = parse(req.headers['content-type'], ';')

		const body = Buffer.concat(chunks).toString('utf-8');
		const lines = body.split('\n');

		for(let i = 4; i < lines.length; i++) {
			console.log(lines[i]);
		}

		console.log(lines);	
		console.log(parsedContentType);
		//const body = Buffer.concat(chunks).split('\n');
		//console.log("BODY", body.toString('utf-8'));
	}

	req.on("end", parseFile);
}

const routes = {
	"/login": handleLogin,
	"/": handleIndex,
	"/upload": handleUpload,
}

const server = http.createServer(function (req, res) {
	const handleRoute = routes[req.url];

	if(!handleRoute) {
		res.end(`Route not found with ${req.url} url.`);
		return;
	}

	handleRoute(req, res);	

});

server.listen(8080);
