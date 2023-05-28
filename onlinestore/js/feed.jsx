import React, { useState, useEffect } from "react";
import Item from "./item";


// The parameter of this function is an object with a string called url inside it.
// url is a prop for the item component.
export default function Feed ({ url }) {
  /* state variables using the useState hook */
   const [items, setItems] = useState([]); 
  

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
  
  // Render item image and item owner
  return (
    <div className="items">
        {items.map((item) => (
            <Item url={item.url} key={item.itemid}/>
        ))}
    </div>
  );
}