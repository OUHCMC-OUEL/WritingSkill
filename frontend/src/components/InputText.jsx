import React, { useState } from 'react'
import { Input, Button } from 'antd'
const { TextArea } = Input

function InputText({ onReceiveData }) {
    const [text, setText] = useState("")
    const [res, setRes] = useState("")
    const [loading, setLoading] = useState(false)

    const handleSubmit = async () => {
        setLoading(true)
        setRes("")
        const response = await fetch("http://localhost:8000/writing/check-grammar/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text }),
        });

        const data = await response.json();
        setRes(data.correct_text)
        onReceiveData(data);
        setLoading(false)
    };

    return (
        <div className='flex flex-col gap-6 w-full '>
            <div className="flex flex-col items-center gap-6 p-10 bg-white rounded-lg shadow-md">
                <TextArea
                    rows={8}
                    placeholder="Please text here"
                    maxLength={1000}
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    className="w-full"
                />
                <Button
                    type="primary"
                    size="large"
                    className="w-full py-4 text-lg"
                    disabled={!text.trim()}
                    loading={loading}
                    onClick={handleSubmit} 
                > Check Grammar</Button>
            </div>
            <div className='w-full'>
                <TextArea 
                    rows={8}
                    value={res}
                    disabled={true}
                    // className={res.trim()?"visible":"invisible"} 
                />
            </div>
        </div>
    )
}

export default InputText
