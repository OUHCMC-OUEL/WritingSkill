import React, { useState } from 'react'
import { Button, Menu, Tabs } from 'antd';

function FixMenu({loading, result, onApply}) {

    function ReviewPanel({ review, suggestion }) {
        return (
            <div className="flex flex-col gap-4 h-full">
                {/* Phần REVIEW */}
                <div className="flex-[6] border rounded-md p-3 bg-gray-50">
                    <h4 className="font-semibold text-sm mb-2 text-gray-700">Review</h4>
                    <div className="text-sm text-gray-600">
                        {review || "Hiện tại không có nhận xét"}
                    </div>
                </div>

                {/* Phần SUGGESTION */}
                <div className="flex-[4] border rounded-md p-3 bg-gray-50">
                    <h4 className="font-semibold text-sm mb-2 text-gray-700"> Suggestion </h4>
                    <div className="text-sm text-gray-600">
                        {suggestion || "Hiện tại không có gợi ý"}
                    </div>
                    <Button
                        type="primary"
                        className='mt-5 float-end'
                        loading={loading}
                        disabled ={!suggestion}
                        onClick = {()=>{onApply(suggestion)}}
                    >
                        Áp dụng
                    </Button>
                </div>
            </div>
        );
    }
    const fixedLable = [
        {
            key: "correctness",
            label: "Correctness",
            children: (
            <ReviewPanel
                review={result?.correctness?.review}
                suggestion={result?.correctness?.suggestion}
            />
            )
        },
        {
            key: "clarity",
            label: "Clarity",
            children: (
            <ReviewPanel
                review={result?.clarity?.review}
                suggestion={result?.clarity?.suggestion}
            />
            )
        },
        {
            key: "engagement",
            label: "Engagement",
            children: (
            <ReviewPanel
                review={result?.engagement?.review}
                suggestion={result?.engagement?.suggestion}
            />
            )
        },
        {
            key: "delivery",
            label: "Delivery",
            children: (
            <ReviewPanel
                review={result?.delivery?.review}
                suggestion={result?.delivery?.suggestion}
            />
            )
        }
    ];
    return (
        <>
            <Tabs
                defaultActiveKey="correctness"
                items={fixedLable}
            />
        </>
    );
}

export default FixMenu