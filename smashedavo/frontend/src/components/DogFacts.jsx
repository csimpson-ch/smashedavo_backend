import React, { useState, useEffect } from 'react';
import '../static/bootstrap.min.css';


function Heading(blogposts) {
    let numberBlogPosts = Object.keys(blogposts).length;
    let lengthCheck = JSON.stringify(blogposts);
    console.log(lengthCheck);
    console.log(blogposts);
    if (numberBlogPosts === 0) {
        return (
            <div>
                <h1>No posts are available</h1>
            </div>
        )
    } else if (numberBlogPosts > 0) {
        return (
            <div>
                <h1>Blog Posts</h1>
            </div>
        )
    } else {
        return (
            <div>
                <h1>Something Else</h1>
            </div>
        )
    }
}


const DogFacts = () => {
    // State to hold the fetched blog posts
    const [blogposts, setBlogposts] = useState([]);

    // let url = 'https://api.openbrewerydb.org/v1/breweries';
    let url = 'http://127.0.0.1:8000/backend/blogposts';

    useEffect(() => {
        fetch(url, {
                method: 'GET',
                modes: 'cors',
                cache: "no-cache",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                },
            }
        )
        .then(response => response.json())
        .then(data => {
            setBlogposts(data)
        })
        .catch(error => console.error(error));
    }, []);
    
    // Render the fetched blog posts
    return (
        <div>
            <Heading
                blogposts={blogposts}
            />

            <ul class="list-group">
                {blogposts.map((blogposts) => (
                    <li class="list-group-item">
                        <h2>{blogposts.fields.title}</h2>
                        <p>{blogposts.fields.text}</p>
                        <p>Posted by {blogposts.fields.user} on {blogposts.fields.pub_date}</p>
                    </li>
                ))}
            </ul>

        </div>
    )
}

export default DogFacts