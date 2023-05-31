import React, { useState, useEffect } from "react";
import Like from "./like";
import moment from "moment";
import Comment from "./comment";
import Container from 'react-bootstrap/Container';
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Card from "react-bootstrap/Card";
import Image from 'react-bootstrap/Image';
import Button from "react-bootstrap/Button";
import Form from 'react-bootstrap/Form';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCartShopping } from "@fortawesome/free-solid-svg-icons";

// The parameter of this function is an object with a string called url inside it.
// url is a prop for the item component.
export default function Item({ url, handleCart }) {
  /* state variables using the useState hook */

  const [imgUrl, setImgUrl] = useState("");
  const [itemid, setItemId] = useState(0);
  const [owner, setOwner] = useState("");
  const [comments, setComments] = useState([]);
  const [lognameLikes, setlognameLikes] = useState(false);
  const [likeUrl, setLikeUrl] = useState("");
  const [numLikes, setNumLikes] = useState(0);
  const [created, setCreated] = useState("");
  const [ownerImgUrl, setOwnerImgUrl] = useState("");
  const [ownerShowUrl, setOwnerShowUrl] = useState("");
  const [newComment, setNewComment] = useState("");
  const [itemurl, setitemUrl] = useState("");
  const [inCart, setInCart] = useState(false);

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
          setImgUrl(data.imgUrl);
          setItemId(data.itemid);
          setOwner(data.owner);
          setComments(data.comments);
          setlognameLikes(data.likes.lognameLikesThis);
          setLikeUrl(data.likes.url);
          setNumLikes(data.likes.numLikes);
          setCreated(data.created);
          setOwnerImgUrl(data.ownerImgUrl);
          setOwnerShowUrl(data.ownerShowUrl);
          setitemUrl(data.itemShowUrl);
            
        }
      })
      .catch((error) => console.log(error));

    return () => {
      // This is a cleanup function that runs whenever the item component
      // unmounts or re-renders. If a item is about to unmount or re-render, we
      // should avoid updating state.
      console.log("test");
      ignoreStaleRequest = true;
    };
  }, [url]);
  // WHEN LIKE/UNLIKE BUTTON IS PRESSED, THIS IS HOW WE HANDLE IT
  function handleLike() {
    if(lognameLikes) {
        fetch(likeUrl, { credentials: "same-origin", method: "DELETE" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
        })
        .then(() => {
          setlognameLikes(!lognameLikes);
          setLikeUrl("");
          setNumLikes(numLikes - 1);
        });
    } else {
        const u = `/api/v1/likes/?itemid=${itemid}`;
        fetch(u, { credentials: "same-origin", method: "POST" })
            .then((response) => {
            if (!response.ok) throw Error(response.statusText);
            return response.json();
            })
            .then((data) => {
            setLikeUrl(data.url);
            setNumLikes(numLikes + 1);
            setlognameLikes(!lognameLikes);
        });
    }
  }
  // NEW COMMENT LOGIC
  function handleText(e) {
    console.log(e.target.value);
    setNewComment(e.target.value);
  }

  function postComment (e) {
    e.preventDefault();
    const comurl = `/api/v1/comments/?itemid=${itemid}`;
    // need to upload JSON data
    fetch(comurl, {
        credentials: "same-origin",
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ newComment }),
    })
    .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
    })
    .then((data) => {
        console.log(data);
        const newCom = {
            commentid: data.commentid,
            lognameOwnsThis: data.lognameOwnsThis,
            ownerShowUrl: data.ownerShowUrl,
            text: data.text,
            url: data.url,
            owner: data.owner,
        };
        setComments([...comments, newCom]);
        setNewComment("");
    });

  }

  function deleteComment (url, commentid) {
    fetch(url, { credentials: "same-origin", method: "DELETE" })
    .then(
        (data) => {
          console.log(data);
          setComments(comments.filter(c => c.commentid !== commentid));
        }
    );
  }
  function added() {
    handleCart(itemid);
    setInCart(true);
  }
  // Render item image and item owner
  return (
    <Container>
        <Row className="justify-content-md-center">
            <Card className="w-25 h-50">
              <Button disabled={inCart} onClick={added} className="m-3"> 
              <FontAwesomeIcon icon={faCartShopping} /> {inCart ? "Added!" : "Add to Cart"}
              </Button>
                <Card.Img variant="top" src={imgUrl} alt="item-image"/>
                <Card.Body>
                    <Row>
                        <Col>
                        <Image fluid rounded className="float-end profile-pic" src={ownerImgUrl}/>
                        </Col>
                        <Col md={6}>
                            <a href={ownerShowUrl}> <p>{owner}</p> </a>
                        </Col>
                        <Col>
                        <a href={itemurl}> <p>{moment.utc(created, "YYYY-MM-DD hh:mm:ss").fromNow()}</p> </a>
                        </Col>
                    </Row>
                    <Container>
                    <Like onClick={handleLike} lognameLikesThis={lognameLikes}
                        numLikes={numLikes}
                    />
                    </Container>
                    <hr/>
                    {
                        comments.map((comment) => (
                            <Container key={comment.commentid}>
                                <Comment onClick={() => deleteComment(comment.url, comment.commentid)} owner={comment.owner} text={comment.text} 
                                lognameCommentedThis={comment.lognameOwnsThis}
                                ownerUrl={comment.ownerShowUrl} />
                            </Container>
                            
                        ))
                    }
                    <hr/>
                    <Row>
                        <Form className="comment-form" onSubmit={postComment}>
                            <Row>
                                <Col>
                                <Form.Control type="text"  value={newComment} onChange={handleText}></Form.Control>
                                </Col>
                                <Col>
                                <Form.Control  type="submit"  name="comment" value="comment"></Form.Control>
                                </Col>   
                            </Row>
                            
                        </Form>
                    </Row>
                </Card.Body>
            </Card>
        </Row>
        
    </Container>
    
  );
}