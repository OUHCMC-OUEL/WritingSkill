import React, { useState } from "react";
import "./App.css";
import InputText from "./components/InputText";
import TextBox from "./components/TextBox";

function App() {
  const [data, setData] = useState(null)

  const handleDataFromChild = (data) => {
      setData(data)
  };
  
  return (
    <div className="flex flex-row justify-center gap-6 p-10 mx-auto">
      <InputText onReceiveData={handleDataFromChild}></InputText>
      <TextBox data={data}></TextBox>
    </div>
  )
}

export default App;
