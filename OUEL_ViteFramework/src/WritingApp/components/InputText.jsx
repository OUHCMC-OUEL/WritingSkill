import React, { useState } from 'react'
import { Input, Button, Alert } from 'antd'
import Marquee from 'react-fast-marquee';
import Apis, { endpoints } from '../utils/Apis'

const { TextArea } = Input

const MAX_LENGTH = 10000

function InputText({ setResult, setLoading, loading, input, setInput }) {
    
    const validate = () => {
        if(!input.trim()){
            <Alert
                banner
                type = {error}
                title={
                <Marquee pauseOnHover gradient={false}>
                    Bạn cần viết ít nhất một từ
                </Marquee>
                }
            />
            return false
        }
        return true
    }

    const handleSubmit = async () => {
        if (!validate()) return
        try{
            setLoading(true)
            setResult("")
            let user_input = {
                input: input
            }

            let temp;
            temp = await Apis.post(endpoints['check-grammar'], user_input)

            setResult(temp.data)
        }  
        catch(ex){
            console.log(ex)
        }
        finally{
            setLoading(false)
        }
    };

    return (
        <div className="flex flex-col gap-7 w-full h-full">
            <div className="flex flex-col items-center gap-8 p-10 h-full">
                <div className="w-full">
                    <div className=" rounded-xl border border-gray-300 bg-white shadow-sm">
                        <TextArea
                            className="w-full h-full resize-none"
                            rows={20}
                            placeholder="Please text here"
                            maxLength={MAX_LENGTH}
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                        />
                    </div>

                    <div className="mt-2 float-end text-sm text-gray-500">
                        <span className={`font-medium ${input.length >= MAX_LENGTH ? 'text-red-500' : ''}`}>
                        {input.length}/{MAX_LENGTH} characters
                        </span>
                    </div>
                </div>

                <Button
                    type="primary"
                    size="large"
                    className="w-full py-4 text-lg"
                    disabled={!input.trim() || input.length>=MAX_LENGTH}
                    loading={loading}
                    onClick={handleSubmit}
                >
                    Check Grammar
                </Button>
            </div>
        </div>
    );
}

export default InputText