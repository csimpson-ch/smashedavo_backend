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



export default function Blog() {
    // State to hold the fetched blog posts
    const [blogposts, setBlogposts] = useState([]);

    const getBlogposts = async () => {

        // let url = 'https://api.openbrewerydb.org/v1/breweries';
        let url = 'https://api.openbrewerydb.org/v1/breweries';

        try {
            // Fetch data from the backend
            const response = await fetch(url, {
                    method: 'GET',
                    modes: 'cors',
                    cache: "no-cache",
                    credentials: "same-origin",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }
            );

            // Parse the response as JSON
            const jsonData = await response.json();

            // Update the state with the fetched data
            setBlogposts(jsonData.blogposts);

        } catch (error) {
            console.error(error);
        }
    }
    useEffect(() => {
        getBlogposts();
    }, []);
    
    // Render the fetched blog posts
    return (
        <div>
            <Heading
                blogposts={blogposts}
            />
            {blogposts.map((blogposts) => (
                <div>
                    <p>{blogposts.name}</p>
                </div>
            ))}


        </div>
    )
}

// export default Blog