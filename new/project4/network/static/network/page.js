function render_pagebar(has_previous, has_next) {
	return (
		<div className="d-flex justify-content-end my-3">
		  <nav aria-label="Page navigation ">
		    <ul className="pagination">
		      { has_previous
			    ? <li className="page-item">
			        <a className="page-link" href="?page={{posts.previous_page_number}}" aria-label="Previous">
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
			  		<a className="page-link" href="?page={{posts.next_page_number}}" aria-label="Next">
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

class Page extends React.Component {

	constructor(props) {
        super(props);

        this.state = { 
        	data: {}, 
        	isFetching: true, 
        	error: null 
        };
    }

	render() {
		fetch('/network')
		.then((response) => {
			return response.json();
		})
	    .then((posts) => this.setState({data: posts, isFetching: false}));

	    const { data, isFetching, error } = this.state;

	    if (isFetching) return <div>...Loading</div>;
	    if (error) return <div>{`Error: ${e.message}`}</div>;

	    let has_next = data[0];
	    data.shift();
	    let has_previous = data[0];
	    data.shift();
	    let requestUser = data[0];
	    data.shift();
	    
	    // console.log(requestUser, data);

		const postsHtml = data.map((post) => {
			return (
				<div class="card my-2" key={post.id}>
				  <div className="card-body my-card">
				    <div className="d-flex mb-2">
				      <div className="d-flex justify-content-start">
				        <a href="{% url 'profile' post.user.username%}">
				          <span className="text-secondary">{post.username}</span>
				        </a>
				      </div>
				      <div className="w-100 d-flex justify-content-end">
				        <span className="mx-2 text-secondary">{post.timestamp}</span>
			        	  { requestUser == post.username
			        	    ? <span className="text-primary edit" data-id="{{post.id}}" id="edit-btn-{{post.id}}">Edit
			        	      </span>
			        	    : null
			        	  }
				      </div>
				    </div>
				    <span id="post-content-{{post.id}}" className="post">{ post.post_name }</span>
				  {/*  <textarea data-id="{{post.id}}" id="post-edit-{{post.id}}" style="display:none;" className="form-control textarea" row="3">
				      { post.post_body }
				    </textarea>*/}
				    <div className="like mt-3">
				     {/*! requestUser in post.like.all*/}
				    	{ true
					      ? <img data-id="{{post.id}}" id="post-like-{{post.id}}" className="liked" data-is_liked="no" src="https://img.icons8.com/carbon-copy/100/000000/like--v2.png" />
						  : <img data-id="{{post.id}}" id="post-like-{{post.id}}" className="liked" data-is_liked="yes" src="https://img.icons8.com/plasticine/100/000000/like.png" />
					    }
				    	{/*<span id="post-count-{{post.id}}">{ post.like.count }</span>*/}
				    </div>
				  </div>
				</div>
			);
		});

		const pages = render_pagebar(has_previous, has_next);

		return (
			<div>
				<h2> All Posts </h2>
				<div className="card">
				  <div className="card-body my-card">
				    Add New Post
				    <textarea className="mt-2 form-control" id="add-text" rows="3"></textarea>
				    <div className="mt-2 d-flex justify-content-end">
				      <button type="submit" id="add-btn" className="btn btn-success">Post</button>
				    </div>
				  </div>
				</div>
				<div id="root"></div>
				{postsHtml}
				{pages}
			</div>
		)
	}
}