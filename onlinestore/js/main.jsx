import React from "react";
import { createRoot } from "react-dom/client";
import Feed from "./feed";
import { BrowserRouter as Router } from 'react-router-dom';
import Site from "./site";
// Create a root
const root = createRoot(document.getElementById("reactEntry"));

// This method is only called once
// Insert the item component into the DOM
root.render(<Router><Site/></Router>);