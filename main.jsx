import React, {useState} from "react";
import {createRoot} from "react-dom/client";
import {BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer} from "recharts";
import "./style.css";

const API = "http://localhost:8000/api/v1";

const initial = {
 company:"Demo Corp", current_assets:250, current_liabilities:180, cash:60,
 total_assets:900, total_liabilities:520, equity:380, revenue:1000,
 ebit:120, net_income:75, operating_cash_flow:105, interest_expense:25,
 inventory:140, accounts_receivable:110, debt:300
};

function App(){
 const [form,setForm]=useState(initial);
 const [result,setResult]=useState(null);
 const [loading,setLoading]=useState(false);
 const [history,setHistory]=useState([]);

 const submit=async(e)=>{
   e.preventDefault(); setLoading(true);
   const body={...form};
   for(const k of Object.keys(body)) if(k!=="company") body[k]=Number(body[k]);
   const r=await fetch(`${API}/predict`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)});
   const data=await r.json(); setResult(data); setHistory(h=>[data,...h].slice(0,8)); setLoading(false);
 };

 return <div className="app">
   <header><div><h1>FinRiskAI</h1><p>AI-Powered Financial Risk Prediction</p></div><span className="badge">ML + FastAPI</span></header>
   <main>
    <section className="card">
      <h2>Financial Statement Input</h2>
      <form onSubmit={submit}>
       {Object.entries(form).map(([k,v])=><label key={k}>{k.replaceAll("_"," ")}
         <input value={v} type={k==="company"?"text":"number"} step="any"
           onChange={e=>setForm({...form,[k]:e.target.value})}/>
       </label>)}
       <button disabled={loading}>{loading?"Predicting...":"Predict Risk"}</button>
      </form>
    </section>

    <section className="card">
      <h2>Risk Assessment</h2>
      {!result ? <div className="empty">Enter financial data to generate a risk assessment.</div> :
      <>
       <div className={`risk ${result.risk_band.toLowerCase()}`}>
        <strong>{result.risk_band} Risk</strong>
        <span>{result.risk_score}/100</span>
       </div>
       <p>Estimated distress probability: <b>{(result.risk_probability*100).toFixed(2)}%</b></p>
       <h3>Model Drivers</h3>
       <ResponsiveContainer width="100%" height={260}>
        <BarChart data={result.explanations}>
          <XAxis dataKey="feature" angle={-20} textAnchor="end" height={70}/>
          <YAxis/><Tooltip/><Bar dataKey="importance"/>
        </BarChart>
       </ResponsiveContainer>
       <ul>{result.explanations.map(x=><li key={x.feature}><b>{x.feature}</b>: {x.value} — {x.interpretation}</li>)}</ul>
       <small>Educational model output; not a credit or investment decision.</small>
      </>}
    </section>
   </main>
   <footer>FinRiskAI • Corporate financial risk analytics</footer>
 </div>
}
createRoot(document.getElementById("root")).render(<App/>);
