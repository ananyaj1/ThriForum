import React, { useState, useEffect } from "react";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Button from "react-bootstrap/Button";
// The parameter of this function is an object with a string called url inside it.
// url is a prop for the item component.
export default function Comment({ onClick, owner, text, lognameCommentedThis, ownerUrl }) {
    


    // Render item image and item owner
    return (
        <Row>
            <Col>
                <p><a href={ownerUrl}>{owner}</a></p>
            </Col>
            <Col>  
                <p>{text}</p> 
            </Col>
           <Col>
            {lognameCommentedThis ? (
                    <Button type="submit" 
                            className="delete-comment-button" 
                            onClick={onClick}>
                        Delete
                    </Button>
                ) 
            : null}
           </Col>
        </Row>
    );
}

