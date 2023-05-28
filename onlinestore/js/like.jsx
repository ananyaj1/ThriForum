import React, { useState, useEffect } from "react";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
// The parameter of this function is an object with a string called url inside it.
// url is a prop for the item component.
export default function Like({ onClick, lognameLikesThis, numLikes}) {
    


  // Render item image and item owner
  return (
        <Row>
            <Col className="align-self-end">
                <p>{numLikes} {numLikes == 1 ? "like" : "likes" } </p>
            </Col>
            <Col className="d-flex justify-content-end">
                <Button type="submit"
                        className="like-unlike-button"
                        onClick={onClick}>
                    {lognameLikesThis ? <p> Unlike </p> : <p> Like </p>}
                </Button>
            </Col>
        </Row>
  );
}
