function render_pagebar(has_previous, has_next) {
	return (
		<div className="d-flex justify-content-end my-3">
		  <nav aria-label="Page navigation ">
		    <ul className="pagination">
		      { has_previous
			    ? <li className="page-item">
			        <a className="page-link" href="#" aria-label="Previous">
			          <span aria-hidden="true">&laquo;</span>
			          <span className="sr-only">Previous</span>
			        </a>
			      </li>
			    : <li className="page-item disabled">
			        <a className="page-link" href="#" aria-label="Previous">
			          <span aria-hidden="true">&laquo;</span>
			          <span className="sr-only">Previous</span>
			        </a>
			      </li>
		      }
			  { has_next
			  	? <li className="page-item">
			  		<a className="page-link" href="#" aria-label="Next">
			  			<span aria-hidden="true">&raquo;</span>
			            <span className="sr-only">Next</span>
			        </a>
			      </li>
			    : <li className="page-item disabled">
			    	<a className="page-link" href="#" aria-label="Next">
			          <span aria-hidden="true">&raquo;</span>
			          <span className="sr-only">Next</span>
			        </a>
			      </li>
		      }
		    </ul>
		  </nav>
		</div>
	);
}

class AllPosts extends React.Component {

	constructor(props) {
	    super(props);
	    this.state = {
	    	post_name: '',
	    	post_body: ''
	    };
	    this.handleSubmit = this.handleSubmit.bind(this);
	    this.handleLike = this.handleLike.bind(this);
	    this.handleUser = this.handleUser.bind(this);
	    this.handleChange1 = this.handleChange1.bind(this);
	    this.handleChange2 = this.handleChange2.bind(this);
	    // this.handleSubmit = this.handleSubmit.bind(this);
	}

	handleSubmit(event) {
		this.props.onClick("addpost", {
				    		name: this.state.post_name,
				    		body: this.state.post_body
				    	});
		this.state.post_name = "";
		this.state.post_body = "";
	    event.preventDefault();
	}

	handleChange1(event) { 
	   this.setState({post_name: event.target.value});
	}

	handleChange2(event) { 
	   this.setState({post_body: event.target.value});
	}

	handleLike(event) {
		alert("Hello world");
	}

	handleUser(user) {
		this.props.onClick("profile", {username: user});
		this.state.post_name = "";
		this.state.post_body = "";
	    event.preventDefault();
	}

	handleEditpost(post) {
		console.log(post.post_name, post.post_body);
		this.props.onClick("editpost", {
							id: post.id,
							user: post.username,
				    		post_name: post.post_name,
				    		post_body: post.post_body
				    	});
		this.state.post_name = "";
		this.state.post_body = "";
	    event.preventDefault();
	}

	render() {
	    
	    // console.log(requestUser, data);

	    const requestUser = this.props.user;
		const postsHtml = this.props.posts.map((post) => {
			return (

				<div className="list-group-item d-flex" key={post.id}>
		    		<div className="d-flex flex-column justify-content-center">
			    		
			        	<a href="#" onClick={()=>this.handleUser( post.username )}>Created by { post.username }</a>
			        	<span id="post-content-{{post.id}}" className="post">Name: { post.post_name }</span>
			        	<p>Content: { post.post_body } </p>
			        	{ requestUser == post.username
				          ? <a href="#" onClick={()=>this.handleEditpost( post )}>Edit</a>
				          : null
				        }
					    <span className="text-secondary">Created: {post.timestamp}</span>
					    
			        	<div className="like">
					     
					    	{ ! post.is_liked
						      ? <a href="#" onClick={()=>this.handleLike()}>
						      		<img data-id="{{post.id}}" id="post-like-{{post.id}}" className="liked" data-is_liked="no" src="https://img.icons8.com/carbon-copy/100/000000/like--v2.png" />
						      	</a>
							  : <a>
									<img data-id="{{post.id}}" id="post-like-{{post.id}}" className="liked" data-is_liked="yes" src="https://img.icons8.com/plasticine/100/000000/like.png" />
								</a>
						    }
					    	{<span id="post-count-{{post.id}}">{ post.count_likes }</span>}
					    </div>
			        </div>
		    	</div>
			);
		});

		const pages = render_pagebar(this.props.prev, this.props.next);

		return (
			<div>
				<h2> All Posts </h2>
				<div className="card">
				  <div className="card-body my-card">
				    Add New Post
				    <form action="#" onSubmit={this.handleSubmit}>
					    <div className="form-group row">
						    <label htmlFor="post" className="col-sm-2 col-form-label">Name</label>
						    <div className="col-sm-10">
						    	<input type="text" className="form-control" id="post" name="post" value={this.state.post_name} onChange={this.handleChange1}/>
						    </div>
						</div>
						<div className="form-group row">
						    <label htmlFor="text" className="col-sm-2 col-form-label">text</label>
						    <div className="col-sm-10">
						    	<textarea type="text" className="form-control" id="text" name="text" value={this.state.post_body} onChange={this.handleChange2}/>
						    </div>
						</div>
					    <button type="submit" className="btn btn-primary">post</button>
				    </form>
				  </div>
				</div>
				<div id="root"></div>
				{postsHtml}
				{pages}
			</div>
		);
	};
}

class StartPage extends React.Component {
	render() {
		return (
			<div>
				<h2> Network. Welcome page. </h2>
				<h3> This page contains different posts. </h3>
			</div>
		)
	}
}

class Network extends React.Component {

	constructor(props) {
		super(props);

		this.state = { 
			history: [
				{
					data: {},
					choose: ""
				}
			],
			stepNumber: 0,
			isFetching: true, 
			error: null 
		};
	    this.handleClick = this.handleClick.bind(this);
	}

	handleClick(choose, data = {}) {
		const history = this.state.history.slice(0, this.state.stepNumber + 1);
		// console.log(choose);
		if (choose == "posts") {
	        fetch('/network')
	            .then(response => response.json())
	            .then(result => this.setState({
		           	history: history.concat([
			        {
			          data: result,
			          choose: "posts"
			        }
			        ]),
	            	stepNumber: history.length,
	            	isFetching: false 
	            }))
	            .catch(e => {
	              console.log(e);
	              this.setState({
	              	history: history.concat([
				        {
				          data: result,
				          choose: "posts"
				        }
			        ]),
			        stepNumber: history.length,
	            	isFetching: false,
	              	error: e 
	              });
	            });
	    } else if (choose == "following") {
	        fetch('/following')
	            .then(response => response.json())
	            .then(result => this.setState({
		           	history: history.concat([
			        {
			          data: result,
			          choose: "following"
			        }
			        ]),
	            	stepNumber: history.length,
	            	isFetching: false 
	            }))
	            .catch(e => {
	              console.log(e);
	              this.setState({
	              	history: history.concat([
				        {
				          data: result,
				          choose: "following"
				        }
			        ]),
			        stepNumber: history.length,
	            	isFetching: false,
	              	error: e 
	              });
	            });
	    } else if (choose == "editpost") {
	    	this.setState({
	           	history: history.concat([
		        {
		          data: data,
		          choose: "editpost"
		        }
		        ]),
	        	stepNumber: history.length,
	        	isFetching: false 
	        });
			// console.log(history);

		} else if (choose == "addpost") {
			
			// console.log(JSON.stringify(data));
	    	fetch('/network', {method: "post", body: JSON.stringify(data)})
	            .then(response => response.json())
	            .then(result => this.setState({
		           	history: history.concat([
			        {
			          data: result,
			          choose: "posts"
			        }
			        ]),
	            	stepNumber: history.length,
	            	isFetching: false 
	            }));

		} else if (choose == "edit") {
			
			// console.log(JSON.stringify(data));
	    	fetch('/editpost', {method: "post", body: JSON.stringify(data)})
	            .then(response => response.json())
	            .then(result => this.setState({
		           	history: history.concat([
			        {
			          data: result,
			          choose: "posts"
			        }
			        ]),
	            	stepNumber: history.length,
	            	isFetching: false 
	            }));

		} else if (choose == "profile") {
			
			// console.log(JSON.stringify(data));
	    	fetch('/profile', {method: "post", body: JSON.stringify(data)})
	            .then(response => response.json())
	            .then(result => this.setState({
		           	history: history.concat([
			        {
			          data: result,
			          choose: "profile"
			        }
			        ]),
	            	stepNumber: history.length,
	            	isFetching: false
	            }));

		} else {
			this.setState({
	           	history: history.concat([
		        {
		          data: {"auth": true},
		          choose: "network"
		        }
		        ]),
            	stepNumber: history.length,
            	isFetching: false 
            });
		}
	}

	componentDidMount() {
		const history = this.state.history.slice(0, this.state.stepNumber + 1);
        fetch('/network')
            .then(response => response.json())
            .then(result => this.setState({
	           	history: history.concat([
		        {
		          data: result,
		          choose: "network"
		        }
		        ]),
            	stepNumber: history.length,
            	isFetching: false 
            }))
            .catch(e => {
              console.log(e);
              this.setState({
              	history: history.concat([
			        {
			          data: result,
			          choose: "network"
			        }
		        ]),
		        stepNumber: history.length,
            	isFetching: false,
              	error: e 
              });
            });
    }

	render() {

		if (this.state.isFetching) return <div>...Loading</div>;
		if (this.state.error) return <div>{`Error: ${e.message}`}</div>;

		const history = this.state.history;
		// console.log(history);
		const choose = history[this.state.stepNumber].choose;
		const data = history[this.state.stepNumber].data;

	    // "next", "prev", "username", "auth", "posts"
	    const nav = 
	    <nav className="navbar navbar-expand-lg navbar-light bg-light">
		    <a className="navbar-brand" href="#" onClick={()=>this.handleClick("network")}>Network</a>
		    { data["auth"]
		      ?
		      	<div>
	              <ul className="navbar-nav mr-auto">
		              <li className="nav-item"><a className="nav-link" href="#" onClick={()=>this.handleClick("user")}><strong>{ data["name"] }</strong></a></li>
		              <li className="nav-item"><a className="nav-link" href="#" onClick={()=>this.handleClick("posts")}>All Posts</a></li>
		              <li className="nav-item"><a className="nav-link" href="#" onClick={()=>this.handleClick("following")}>Following</a></li>
		              <li className="nav-item"><a className="nav-link" href="/logout">Log Out</a></li>
		      	  </ul>
	            </div>
		      :
		      	<div>
	              <ul className="navbar-nav mr-auto">
		              <li className="nav-item"><a className="nav-link" href="#" onClick={() => this.handleClick("posts")}>All Posts</a></li>
		              <li className="nav-item"><a className="nav-link" href="/login">Log In</a></li>
		              <li className="nav-item"><a className="nav-link" href="/register">Reister</a></li>
		      	  </ul>
	            </div>
		    }
		</nav>

		if (choose == "posts") {
			return ( 
				<div className="Network"> 
					{nav} 
					<AllPosts 
						posts={data["posts"]} 
						next={data["next"]}
						prev={data["prev"]}
						user={data["username"]}
						onClick={(choose, data={})=>this.handleClick(choose, data)}
					/> 
				</div>
			)
		} else if (choose == "editpost") {
			return ( 
				<div className="Editpost"> 
					{nav} 
					<Editpost
						data={data}
						onClick={(choose, data={})=>this.handleClick(choose, data)}
					/>
				</div>
			)
		} else if (choose == "following") {
			return ( 
				<div className="Following"> 
					{nav} 
					<Following
						posts={data["posts"]} 
						next={data["next"]}
						prev={data["prev"]}
						user={data["username"]}
						onClick={(choose, data={})=>this.handleClick(choose, data)}
					/>
				</div>
			)
		} else if (choose == "profile") {
			return ( 
				<div className="Profile"> 
					{nav} 
					<Profile
						data={data}
					/>
				</div>
			)
		} else {
			return ( 
				<div className="Network"> 
					{nav} 
					<StartPage/>
				</div>
			)
		}
	}
}

class Profile extends React.Component {
	constructor(props) {
	    super(props);
	}

	render() {

	  const requestUser = this.props.data["user"];
		const postsHtml = this.props.data["posts"].map((post) => {
			return (

				<div className="list-group-item d-flex" key={post.id}>
		    		<div className="d-flex flex-column justify-content-center">
			    		
			        	<a href="#" onClick={()=>this.handleUser( post.username )}>Created by { post.username }</a>
			        	<span id="post-content-{{post.id}}" className="post">Name: { post.post_name }</span>
			        	<p>Content: { post.post_body } </p>
			        	{ requestUser == post.username
				          ? <span className="text-primary edit" data-id="{{post.id}}" id="edit-btn-{{post.id}}">Edit
				            </span>
				          : null
				        }
					    <span className="text-secondary">Created: {post.timestamp}</span>
					    
			        	<div className="like">
					     
					    	{ ! post.is_liked
						      ? <a href="#" onClick={()=>this.handleLike()}>
						      		<img data-id="{{post.id}}" id="post-like-{{post.id}}" className="liked" data-is_liked="no" src="https://img.icons8.com/carbon-copy/100/000000/like--v2.png" />
						      	</a>
							  : <a>
									<img data-id="{{post.id}}" id="post-like-{{post.id}}" className="liked" data-is_liked="yes" src="https://img.icons8.com/plasticine/100/000000/like.png" />
								</a>
						    }
					    	{<span id="post-count-{{post.id}}">{ post.count_likes }</span>}
					    </div>
			        </div>
		    	</div>
			);
		});

		const pages = render_pagebar(this.props.data["prev"], this.props.data["next"]);

		return (
			<div>
				<h2> Profile </h2>
				<div className="card">
				  <div className="card-body my-card"> User: {this.props.data["user_post"]}</div>
				  <div className="card-body my-card"> Count followers: {this.props.data["count_followers"]}</div>
				  <div className="card-body my-card"> Count followings: {this.props.data["count_followings"]}</div>

				  <button class="btn btn-outline-primary mx-2 h-25" data-user="{{user.username}}">
				  Follow </button>

				</div>
				<div id="root"></div>
				{postsHtml}
				{pages}
			</div>
		);
	};
}

class Editpost extends React.Component {
	constructor(props) {
	    super(props);
	    this.state = {
	    	post_id: this.props.data["id"],
	    	post_name: this.props.data["post_name"],
	    	post_body: this.props.data["post_body"]
	    };
	    this.handleSubmit = this.handleSubmit.bind(this);
	    this.handleChange1 = this.handleChange1.bind(this);
	    this.handleChange2 = this.handleChange2.bind(this);
	}

	handleSubmit(event) {
		this.props.onClick("edit", {
							id: this.state.post_id,
				    		name: this.state.post_name,
				    		body: this.state.post_body
				    	});
	    event.preventDefault();
	}

	handleChange1(event) { 
	   this.setState({post_name: event.target.value});
	}

	handleChange2(event) { 
	   this.setState({post_body: event.target.value});
	}

	render() {

		return (
			<div>
				<div className="card">

				  <div className="card-body my-card">
				    Edit post
				    <form action="#" onSubmit={this.handleSubmit}>
				    	<h4> User: {this.props.data["user"]} </h4>
					    <div className="form-group row">
						    <label htmlFor="post" className="col-sm-2 col-form-label">Name</label>
						    <div className="col-sm-10">
						    	<input type="text" className="form-control" id="post" name="post" value={this.state.post_name} onChange={this.handleChange1}/>
						    </div>
						</div>
						<div className="form-group row">
						    <label htmlFor="text" className="col-sm-2 col-form-label">text</label>
						    <div className="col-sm-10">
						    	<textarea type="text" className="form-control" id="text" name="text" value={this.state.post_body} onChange={this.handleChange2}/>
						    </div>
						</div>
					    <button type="submit" className="btn btn-primary">post</button>
				    </form>
				  </div>
				</div>
			</div>
		);
	};
}


class Following extends React.Component {

	constructor(props) {
	    super(props);
	    this.handleLike = this.handleLike.bind(this);
	    this.handleUser = this.handleUser.bind(this);
	}

	handleLike(event) {
		alert("Hello world");
	}

	handleUser(user) {
		this.props.onClick("profile", {username: user});
		this.state.post_name = "";
		this.state.post_body = "";
	    event.preventDefault();
	}

	handleEditpost(post) {
		this.props.onClick("editpost", {
							id: post.id,
							user: post.username,
				    		post_name: post.post_name,
				    		post_body: post.post_body
				    	});
		this.state.post_name = "";
		this.state.post_body = "";
	    event.preventDefault();
	}

	render() {

	    const requestUser = this.props.user;
		const postsHtml = this.props.posts.map((post) => {
			return (

				<div className="list-group-item d-flex" key={post.id}>
		    		<div className="d-flex flex-column justify-content-center">
			    		
			        	<a href="#" onClick={()=>this.handleUser( post.username )}>Created by { post.username }</a>
			        	<span id="post-content-{{post.id}}" className="post">Name: { post.post_name }</span>
			        	<p>Content: { post.post_body } </p>
			        	{ requestUser == post.username
				          ? <a href="#" onClick={()=>this.handleEditpost( post )}>Edit</a>
				          : null
				        }
					    <span className="text-secondary">Created: {post.timestamp}</span>
					    
			        	<div className="like">
					     
					    	{ ! post.is_liked
						      ? <a href="#" onClick={()=>this.handleLike()}>
						      		<img data-id="{{post.id}}" id="post-like-{{post.id}}" className="liked" data-is_liked="no" src="https://img.icons8.com/carbon-copy/100/000000/like--v2.png" />
						      	</a>
							  : <a>
									<img data-id="{{post.id}}" id="post-like-{{post.id}}" className="liked" data-is_liked="yes" src="https://img.icons8.com/plasticine/100/000000/like.png" />
								</a>
						    }
					    	{<span id="post-count-{{post.id}}">{ post.count_likes }</span>}
					    </div>
			        </div>
		    	</div>
			);
		});

		const pages = render_pagebar(this.props.prev, this.props.next);

		return (
			<div>
				<h2> Following Posts </h2>
				<div id="root"></div>
				{postsHtml}
				{pages}
			</div>
		);
	};
}

ReactDOM.render(
  <Network />,
  document.getElementById('root')
);