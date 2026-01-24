import { useState } from 'react';
import InputText from "../components/InputText";
import FixMenu from "../components/FixMenu";
import { Alert, Modal } from 'antd';

function WritingApp() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [input, setInput] = useState("");

  const applySuggestion = (suggestion) => {
    if (!suggestion) return;
  
    if (suggestion === input) {
      Modal.info({
        title: "Thông báo",
        content: "Gợi ý này giống với nội dung hiện tại."
      });
      return;
    }

    Modal.confirm({
      title: "Bạn muốn áp dụng gợi ý này?",
      content: "Nội dung hiện tại sẽ được thay thế.",
      closable: true,
      okText: "Áp dụng",
      cancelText: "Huỷ",
      onOk: () => setInput(suggestion)
    });
  };
  
  return (
    <>
      <h3 className="text-center py-8 text-2xl font-bold text-gray-800">
        ENHANCE YOUR WRITING SKILL
      </h3>
      
      <div className="mx-auto px-5">
        <div className="flex gap-6">

          {/* PHẦN VIẾT */}
          <div className="flex-[7]">
            <InputText 
                setResult={setResult}
                setLoading={setLoading} 
                loading={loading}
                input = {input}
                setInput = {setInput}
            />
          </div>

          {/* PHẦN SỬA LỖI */}
          <div className="flex-[3] border-l border-gray-300 pl-6">
           <FixMenu loading={loading} result= {result} onApply={applySuggestion}/>
          </div>

        </div>
      </div>
    </>
)
}

export default WritingApp;