import React, { useState, useEffect } from "react";
import { Routes, Route } from 'react-router-dom';
import Feed from "./feed";
import Cart from "./cart";
// The parameter of this function is an object with a string called url inside it.
// url is a prop for the item component.
export default function Site({ }) {
    


    // Render item image and item owner
    return (
        <div>
            <Routes>
                <Route exact path="/*" element={<Feed url="/api/v1/posts/"/>}/>
                <Route path="cart" element={<Cart/>}/>
            </Routes>
        </div>
    );
}