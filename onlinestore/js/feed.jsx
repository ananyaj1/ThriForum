import React, { useState, useEffect } from "react";
import Item from "./item";
import Container from 'react-bootstrap/Container';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Navbar from "react-bootstrap/Navbar"
import Image  from "react-bootstrap/Image";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
// The parameter of this function is an object with a string called url inside it.
// url is a prop for the item component.
export default function Feed ({ url }) {
  /* state variables using the useState hook */
   const [items, setItems] = useState([]); 
   const [cart, setCart] = useState([]);
   const [logname, setLogname] = useState("");


  useEffect(() => {
    // Declare a boolean flag that we can use to cancel the API request.
    let ignoreStaleRequest = false;
    
    // Call REST API to get the item's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        // If ignoreStaleRequest was set to true, we want to ignore the results of the
        // the request. Otherwise, update the state to trigger a new render.
        if (!ignoreStaleRequest) {
          console.log(data);
          setItems(data.results);
          setLogname(data.logname);
        }
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the item component
      // unmounts or re-renders. If a item is about to unmount or re-render, we
      // should avoid updating state.
      ignoreStaleRequest = true;
      
    };
  }, [url]);
  // WHEN LIKE/UNLIKE BUTTON IS PRESSED, THIS IS HOW WE HANDLE IT
  function handleCart(itemid) {
    
    setCart([...cart, itemid]);
    
    console.log(cart);
  }

  const u = `users/${logname}`;
  // Render item image and item owner
  return (
    <div className="home">
      <Navbar className="navbar-expand-lg navbar-light bg-light">
        <Container>
          <Col xs="8" md="8" lg="8">
            <a className="navbar-brand" href="/">
              <Image src="static/thriforum.svg" width="30" height="30" className="d-inline-block align-top" alt=""/>
            </a>
            <Button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
              <span className="navbar-toggler-icon"></span>
            </Button>
            <div className="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div className="navbar-nav">
                  <a className="nav-item nav-link active" href="/"> Home <span className="sr-only"></span></a>
                  <a className="nav-item nav-link" href="/explore/">Explore</a>
                  <a className="nav-item nav-link" href={u}> {logname} </a>
                </div>
            </div>
          </Col>
          <Col>
          <Form className="w-25 ms-auto" action="/accounts/logout" method="post" encType="multipart/form-data">
            <Form.Control type="submit" name="logout" value="Logout" className="btn btn-danger"></Form.Control>
          </Form>
          </Col>
        </Container>

      </Navbar>

      <div className="items">
        {items.map((item) => (
              <Item url={item.url} key={item.itemid} handleCart={handleCart}/>
          ))}
      </div>
     
    </div>
  );
}