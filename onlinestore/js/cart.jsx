import React, { useState } from "react";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import Container from "react-bootstrap/Container";
import { useLocation } from "react-router-dom";
import { Button } from "react-bootstrap";
// The parameter of this function is an object with a string called url inside it.
// url is a prop for the item component.
export default function Cart({ }) {
    const location = useLocation();
    const [cart, setCart] = useState(location.state.cart);
    const [logname, setLogname] = useState(location.state.logname);

    function clearCart() {
        const emptyList = [];
        setCart(emptyList);
    }
    function clearItem(i) {
        setCart(cart.filter(c => c.itemid != i));
    }
    // Render item image and item owner
    return (
        <Container className="vh-100">
            <Row className="justify-content-between text-end">
                <Col><h3>{logname}'s Shopping Cart</h3></Col>
                <Col><Button className="btn-danger" onClick={() => clearCart()}> Remove All </Button> </Col>
            </Row>
            <Container className="text-center">
                {cart.map((item) => (
                    <Row key={item.itemid} className="align-items-center">
                        <Col>
                        <img src={item.imgurl} className="img-fluid rounded float-start h-50"/>
                        </Col>
                        <Col>
                        <h3>{item.name}</h3>
                        </Col>
                        <Col>
                        <Button className="btn-danger" onClick={() => clearItem(item.itemid)}>Delete</Button>
                        </Col>
                        <Col><h3>${item.price}0</h3></Col>
                    </Row>
                ))}
                <br/>
                <Row>
                    <Col>
                     Replace with calculated total
                    </Col>
                </Row>
            </Container>
                
        </Container>
        
    );
}
