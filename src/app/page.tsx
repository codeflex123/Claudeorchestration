"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { 
  CheckCircle, 
  Layout, 
  Globe, 
  FileText, 
  Plus, 
  Search, 
  Grid, 
  Code as CodeIcon, 
  History, 
  Settings, 
  ArrowRight, 
  Maximize2, 
  Mic, 
  Maximize, 
  Box, 
  ChevronDown, 
  Sparkles, 
  AlignLeft, 
  Volume2,
  ChevronRight
} from "lucide-react";

// --- Components ---

const Sidebar = ({ activePrompt, onNewChat }: { activePrompt?: string, onNewChat?: () => void }) => (
  <div style={{ width: '260px', height: '100vh', backgroundColor: '#0d0d0d', display: 'flex', flexDirection: 'column', borderRight: '1px solid rgba(255,255,255,0.05)', zIndex: 50 }}>
    <div className="p-4 pt-6">
      <div className="flex items-center gap-2 px-2 text-white/90">
        <span className="text-xl font-serif font-medium tracking-tight">Claude</span>
        <div className="h-4 w-4 ml-auto opacity-40">
           <Maximize size={16} />
        </div>
      </div>
    </div>

    <div style={{ flex: 1, overflowY: 'auto', paddingLeft: '8px', paddingRight: '8px', paddingTop: '8px', paddingBottom: '8px', display: 'flex', flexDirection: 'column', gap: '2px' }}>
      <button 
        onClick={onNewChat}
        className="flex items-center gap-3 px-3 py-2 text-[13px] text-gray-400 hover:bg-white/5 rounded-lg transition-colors group text-left w-full"
      >
        <Plus className="w-4 h-4" /> New chat
      </button>
      <button className="flex items-center gap-3 px-3 py-2 text-[13px] text-gray-400 hover:bg-white/5 rounded-lg transition-colors">
        <Search className="w-4 h-4" /> Search
      </button>
      <button className="flex items-center gap-3 px-3 py-2 text-[13px] text-gray-400 hover:bg-white/5 rounded-lg transition-colors">
        <History className="w-4 h-4 opacity-70" /> Chats
      </button>
      <button className="flex items-center gap-3 px-3 py-2 text-[13px] text-gray-400 hover:bg-white/5 rounded-lg transition-colors">
        <Grid className="w-4 h-4 opacity-70" /> Projects
      </button>
      <button className="flex items-center gap-3 px-3 py-2 text-[13px] text-gray-400 hover:bg-white/5 rounded-lg transition-colors">
        <FileText className="w-4 h-4 opacity-70" /> Artifacts
      </button>
      <button className="flex items-center gap-3 px-3 py-2 text-[13px] text-gray-400 hover:bg-white/5 rounded-lg transition-colors group">
        <CodeIcon className="w-4 h-4 opacity-70" /> Code <span className="ml-auto text-[9px] text-gray-500 border border-white/10 px-1.5 py-0.5 rounded uppercase font-bold tracking-wider group-hover:text-white group-hover:border-white/20 transition-colors">Upgrade</span>
      </button>
      <button className="flex items-center gap-3 px-3 py-2 text-[13px] text-gray-400 hover:bg-white/5 rounded-lg transition-colors">
        <Settings className="w-4 h-4 opacity-70" /> Customize
      </button>
      <button className="flex items-center gap-3 px-3 py-2 text-[13px] text-gray-400 hover:bg-white/5 rounded-lg transition-colors">
        <AlignLeft className="w-4 h-4 opacity-70" /> Design
      </button>
      <button className="flex items-center gap-3 px-3 py-2 text-[13px] text-gray-400 hover:bg-white/5 rounded-lg transition-colors">
        <ChevronDown className="w-4 h-4 opacity-70" /> More
      </button>

      <div className="mt-8 px-3">
        <span className="text-[10px] font-bold text-gray-600 uppercase tracking-widest">Recents</span>
        <div className="mt-4 flex flex-col gap-0.5">
           <div className="px-3 py-2 text-[13px] text-gray-500 truncate hover:text-white cursor-pointer transition-colors">Creating a Reddit post</div>
           <div className="px-3 py-2 text-[13px] text-gray-500 truncate hover:text-white cursor-pointer transition-colors">AI agent characteristics and tool r...</div>
           <div className="px-3 py-2 text-[13px] text-gray-500 truncate hover:text-white cursor-pointer transition-colors">Python code quiz</div>
           <div className="px-3 py-2 text-[13px] text-gray-500 truncate hover:text-white cursor-pointer transition-colors">Understanding Claude agent</div>
           <div className="px-3 py-2 text-[13px] text-gray-500 truncate hover:text-white cursor-pointer transition-colors">Analyzer markdown overview</div>
           <div className="px-3 py-2 text-[13px] text-gray-500 truncate hover:text-white cursor-pointer transition-colors">Greeting</div>
           {activePrompt && (
             <div className="px-3 py-2 text-[13px] text-white bg-white/5 rounded-lg truncate mt-2">{activePrompt}</div>
           )}
        </div>
      </div>
    </div>

    <div className="mt-auto p-4 flex items-center gap-3 border-t border-white/5">
       <div className="w-8 h-8 rounded-lg bg-[#3b82f6] flex items-center justify-center text-xs font-bold text-white">U</div>
       <div className="flex-1">
          <div className="text-[13px] font-medium text-white/90">User</div>
          <div className="text-[11px] text-gray-500">Pro plan</div>
       </div>
       <div className="w-5 h-5 rounded-full bg-white/5 flex items-center justify-center border border-white/10">
          <ChevronRight className="w-3 h-3 text-gray-500" />
       </div>
    </div>
  </div>
);

const Tag = ({ icon, name }: { icon: React.ReactNode, name: string }) => (
  <div className="px-4 py-2 bg-white/[0.03] rounded-full border border-white/5 text-[12px] text-gray-400 hover:bg-white/10 hover:text-white cursor-pointer transition-all flex items-center gap-2.5">
     <span className="opacity-50">{icon}</span> {name}
  </div>
);

const ClaudeCodeSimulation = ({ bundle, onExit }: any) => (
  <div className="flex-1 flex flex-col bg-[#0b0b0b] font-mono text-[13px] leading-relaxed h-screen overflow-hidden overflow-y-auto">
    <div className="p-3 border-b border-white/5 bg-[#0d0d0d] flex justify-between items-center text-[#ff9089]">
       <span className="font-bold">Claude Code v2.1.112</span>
       <button onClick={onExit} className="text-[10px] text-gray-600 hover:text-white uppercase tracking-widest">exit</button>
    </div>
    
    <div className="p-10 space-y-8 max-w-5xl">
       {/* Welcome Box */}
       <div className="border border-white/10 p-8 rounded-xl bg-black/20 flex gap-12">
          <div className="space-y-6">
             <div className="text-2xl font-bold text-white">Welcome back User!</div>
             <div className="flex flex-col gap-1">
                <div className="w-12 h-10 bg-[#ff9089] rounded relative overflow-hidden flex flex-col items-center justify-center p-2">
                   <div className="w-6 h-4 bg-black/80 rounded-sm"></div>
                   <div className="flex gap-1 mt-1">
                      <div className="w-1.5 h-1.5 bg-black/80"></div>
                      <div className="w-1.5 h-1.5 bg-black/80"></div>
                   </div>
                </div>
                <div className="text-[11px] text-[#ff9089] mt-2 font-bold tracking-tight">
                   Sonnet 4.7 • Claude Pro
                </div>
                <div className="text-[10px] text-white/30 truncate">user@claude.ai's Organization</div>
             </div>
          </div>
          <div className="flex-1 border-l border-white/5 pl-12 space-y-4">
             <div className="text-gray-500 uppercase text-[10px] tracking-[0.2em] font-bold">Tips for getting started</div>
             <div className="text-gray-400 leading-relaxed italic">
                Run <span className="text-white">/init</span> to create a CLAUDE.md file with instructions for Claude.
                <br />
                Note: You have launched claude in your home directory.
             </div>
          </div>
       </div>

       <div className="space-y-4">
          <div className="text-white flex items-center gap-3">
             <span className="text-gray-500">❯</span> 
             {bundle.initial_prompt}
          </div>
          <div className="text-[#ff9089] animate-pulse font-bold text-[11px] uppercase tracking-widest">
             ＊ Synthesizing... (thinking)
          </div>
       </div>

       <div className="space-y-3 pt-4">
          {bundle.metadata.mcp_context && bundle.metadata.mcp_context.map((mcp: any, idx: number) => (
            <div key={idx} className="flex flex-col gap-1">
               <div className="flex gap-3 items-center">
                 <div className="w-1.5 h-1.5 rounded-full bg-white"></div>
                 <span className="text-white/90">Let me search for information regarding: "{bundle.initial_prompt.substring(0, 60)}..."</span>
               </div>
               <div className="flex gap-3 items-center pl-1.5 border-l border-white/10 ml-[3px] py-1">
                 <span className="text-white/40">Web Search("{bundle.initial_prompt.substring(0, 40)} latest updates")</span>
               </div>
               <div className="flex gap-3 items-center pl-4 text-white/40 italic">
                  └ Did 1 search in 11s
               </div>
            </div>
          ))}
          
          <div className="flex gap-3 items-center text-white/90">
             <div className="w-1.5 h-1.5 rounded-full bg-white"></div>
             <span>Good, I have the research. Now let me compose the summary.</span>
          </div>

          <div className="text-gray-400 whitespace-pre-wrap mt-8 leading-relaxed font-sans text-lg italic bg-white/5 p-6 rounded-xl border border-white/5">
             {bundle.system_directive}
          </div>
       </div>
    </div>

    <div className="mt-auto border-t border-white/5 p-3 px-6 bg-[#0d0d0d] flex items-center justify-between text-[10px] text-gray-500 italic">
      <span>esc to interrupt</span>
      <div className="flex gap-6">
        <span className="text-yellow-500 font-bold uppercase tracking-widest not-italic">1 claude.ai connector needs auth</span>
        <span>/mcp</span>
      </div>
    </div>
  </div>
);

const ClaudeCoworkSimulation = ({ bundle, onExit }: any) => (
  <div style={{ flex: 1, display: 'flex', height: '100vh', backgroundColor: '#111111' }}>
     {/* Cowork Left Narrow Sidebar */}
     <div style={{ width: '64px', backgroundColor: '#0d0d0d', borderRight: '1px solid rgba(255,255,255,0.05)', display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: '24px', gap: '24px' }}>
        <div className="w-8 h-8 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-gray-500">
           <History size={18} />
        </div>
        <div className="w-8 h-8 rounded-lg bg-blue-500/10 border border-blue-500/20 flex flex-col items-center justify-center text-blue-400 gap-0.5">
           <Box size={14} />
           <span className="text-[6px] font-bold uppercase truncate">Cowork</span>
        </div>
        <div className="w-8 h-8 rounded-lg bg-white/5 border border-white/10 flex items-center justify-center text-gray-500">
           <CodeIcon size={18} />
        </div>
     </div>

     {/* Main Chat Area */}
     <div style={{ flex: 1, display: 'flex', flexDirection: 'column', borderRight: '1px solid rgba(255,255,255,0.05)' }}>
        <div style={{ padding: '12px 32px', borderBottom: '1px solid rgba(255,255,255,0.05)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
           <div className="flex items-center gap-2">
              <span className="text-[13px] text-white/90 font-medium truncate max-w-md">{bundle.initial_prompt}</span>
              <ChevronDown size={14} className="text-gray-600" />
           </div>
           <button onClick={onExit} className="text-[10px] text-gray-500 hover:text-white uppercase tracking-widest font-bold">exit</button>
        </div>

        <div style={{ flex: 1, overflowY: 'auto', padding: '48px 0' }}>
            <div className="max-w-2xl mx-auto w-full space-y-12 px-8">
               <div className="flex justify-end">
                  <div className="max-w-xl bg-[#222222] p-5 px-7 rounded-[2rem] text-[15px] text-white font-medium">
                     {bundle.initial_prompt}
                  </div>
               </div>

               <div className="space-y-8">
                  <div className="flex flex-col gap-4">
                     <span className="text-[11px] text-gray-500 font-bold uppercase tracking-widest">Loaded tools {'>'}</span>
                     <div className="text-[16px] text-white/90 leading-relaxed italic font-medium">
                        Initiating research for: "{bundle.initial_prompt.substring(0, 80)}..."
                     </div>
                  </div>

                  <div className="flex flex-col gap-4">
                     <span className="text-[11px] text-gray-500 font-bold uppercase tracking-widest">Synthesizing {'>'}</span>
                     <div className="text-[16px] text-white/90 leading-relaxed italic font-medium">
                        Compiling intelligence into a structured orchestration strategy.
                     </div>
                  </div>

                  <div className="p-8 bg-white/[0.02] border border-white/5 rounded-[2.5rem] space-y-6">
                     <div className="flex items-center gap-3 text-[11px] font-bold text-blue-400 uppercase tracking-widest">
                        <Globe size={14} /> System Plan Ready
                     </div>
                     <div className="text-gray-300 leading-relaxed italic font-serif text-lg opacity-80 whitespace-pre-wrap">
                        {bundle.system_directive}
                     </div>
                  </div>
               </div>
            </div>
        </div>

        <div style={{ padding: '24px 32px 48px' }}>
           <div className="max-w-2xl mx-auto bg-[#1a1a1a] border border-white/10 p-4 px-6 rounded-[2.5rem] flex items-center gap-4 relative">
             <Plus className="w-5 h-5 text-gray-500" />
             <div className="flex-1 text-sm text-gray-500">Reply to Cowork...</div>
             <div className="flex items-center gap-4 text-gray-600">
                <span className="text-[11px] font-bold">Sonnet 4.7</span>
                <ChevronDown size={12} />
                <Volume2 className="w-4 h-4" />
             </div>
           </div>
        </div>
     </div>

     {/* Cowork Right Panel */}
     <div style={{ width: '300px', backgroundColor: '#0d0d0d', display: 'flex', flexDirection: 'column', padding: '24px', gap: '32px' }}>
        <div className="space-y-6">
           <div className="flex justify-between items-center px-1">
              <span className="text-[11px] font-bold text-white/40 uppercase tracking-widest">Progress</span>
              <ChevronDown className="w-4 h-4 text-gray-600" />
           </div>
           <div className="flex gap-2 items-center justify-between px-2">
              <div className="w-6 h-6 rounded-full bg-blue-500/20 border border-blue-500/40 flex items-center justify-center"><CheckCircle size={12} className="text-blue-400" /></div>
              <div className="flex-1 h-[1px] bg-white/5"></div>
              <div className="w-6 h-6 rounded-full bg-blue-500/20 border border-blue-500/40 flex items-center justify-center animate-pulse"><div className="w-1.5 h-1.5 rounded-full bg-blue-400" /></div>
              <div className="flex-1 h-[1px] bg-white/5"></div>
              <div className="w-6 h-6 rounded-full border border-white/10"></div>
           </div>
           <div className="text-[10px] text-gray-500 text-center uppercase tracking-widest font-bold opacity-60">See task progress for longer tasks</div>
        </div>

        <div className="space-y-6">
           <div className="flex justify-between items-center px-1">
              <span className="text-[11px] font-bold text-white/40 uppercase tracking-widest">Working folder</span>
              <ChevronRight className="w-4 h-4 text-gray-600" />
           </div>
           <div className="p-4 bg-white/5 rounded-2xl border border-white/5 text-[11px] text-gray-300 font-mono">
              /Users/project
           </div>
        </div>

        <div className="space-y-6">
           <div className="flex justify-between items-center px-1">
              <span className="text-[11px] font-bold text-white/40 uppercase tracking-widest">Context</span>
              <ChevronDown className="w-4 h-4 text-gray-600" />
           </div>
           <div className="space-y-2">
             <div className="flex items-center gap-3 p-4 bg-white/5 rounded-2xl border border-white/5 hover:border-white/10 cursor-pointer transition-colors group">
                <Globe className="w-4 h-4 text-gray-500 group-hover:text-blue-400" />
                <div className="flex flex-col">
                   <span className="text-[11px] font-bold text-gray-300">Web search</span>
                   <span className="text-[9px] text-gray-600 uppercase font-black tracking-tighter">Connector</span>
                </div>
             </div>
           </div>
        </div>
     </div>
  </div>
);

const ClaudeAIView = ({ bundle, onExit }: any) => (
  <div style={{ flex: 1, display: 'flex', flexDirection: 'column', height: '100vh', backgroundColor: '#111111' }}>
     <div style={{ padding: '12px 32px', borderBottom: '1px solid rgba(255,255,255,0.05)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div className="flex items-center gap-2">
           <span className="text-[13px] text-gray-400 font-medium truncate max-w-md">{bundle.initial_prompt}</span>
           <ChevronDown size={14} className="text-gray-600" />
        </div>
        <button className="px-3 py-1.5 bg-white/5 text-[11px] font-bold rounded-lg border border-white/10 text-gray-300 hover:bg-white/10 transition-colors">Share</button>
     </div>
     
     <div style={{ flex: 1, overflowY: 'auto', padding: '48px 0' }}>
        <div className="max-w-3xl mx-auto w-full space-y-12 px-8">
           {/* User Message */}
           <div className="flex justify-end">
              <div className="max-w-2xl bg-[#1e1e1e] p-5 px-7 rounded-[2rem] text-[15px] text-white/90 leading-relaxed">
                 {bundle.initial_prompt}
              </div>
           </div>
           
           {/* AI Response */}
           <div className="space-y-6">
              <div className="flex items-center gap-2 text-[11px] font-bold text-gray-500 uppercase tracking-widest">
                 <span>Searched the web</span>
                 <ChevronRight size={12} />
              </div>

              <div className="text-[16px] text-white/90 font-medium leading-relaxed uppercase tracking-tight">
                 Analyzing your request: "{bundle.initial_prompt.substring(0, 60)}..."
              </div>

              {/* Artifact Card: Email Summary */}
              <div className="bg-[#181818] border border-white/10 rounded-2xl overflow-hidden shadow-xl max-w-2xl">
                 <div className="p-6 space-y-6">
                    <div className="flex items-center gap-3 text-[13px] text-gray-400">
                       <span className="font-bold">Subject:</span>
                       <span className="flex items-center gap-2">
                          <Globe size={14} className="text-blue-400" />
                          Summary: Optimized Strategy for "{bundle.initial_prompt.substring(0, 40)}..."
                       </span>
                    </div>

                    <div className="pt-4 border-t border-white/5 space-y-4 text-[14px] text-gray-300 leading-relaxed">
                       <p>Hi,</p>
                       <p>Here is a concise summary of the research findings regarding your request:</p>
                       
                       <div className="space-y-4 pt-2">
                          <div className="flex items-center gap-3 text-blue-400 font-bold uppercase tracking-wider text-[11px]">
                             <Layout size={14} />
                             LANDMARK CHANGE: NEW INCOME TAX ACT 2025
                          </div>
                          <p className="pl-7">The Income Tax Act, 2025 (replacing the 60-year-old Income Tax Act, 1961) has come into force from 1st April 2026. The new Act simplifies taxation language and compliance.</p>
                       </div>

                       <div className="space-y-4 pt-2">
                          <div className="flex items-center gap-3 text-[#d97757] font-bold uppercase tracking-wider text-[11px]">
                             <Box size={14} />
                             PERSONAL INCOME TAX CHANGES (FY 2025-26)
                          </div>
                          <ul className="pl-7 list-disc space-y-1">
                             <li>Basic Exemption Limit raised from ₹3 lakh → ₹4 lakh (New Tax Regime)</li>
                             <li>Section 87A Rebate increased from ₹25,000 → ₹60,000</li>
                          </ul>
                       </div>
                    </div>
                 </div>

                 <div className="bg-black/20 p-3 px-6 border-t border-white/5 flex justify-end gap-3">
                    <div className="p-2 hover:bg-white/5 rounded-lg cursor-pointer transition-colors text-gray-500 hover:text-white">
                       <Layout size={16} />
                    </div>
                    <button className="flex items-center gap-2 py-1.5 px-4 bg-white/5 border border-white/10 rounded-xl text-[11px] font-bold text-gray-400 hover:bg-white/10 hover:text-white transition-all">
                       <Globe size={14} className="text-blue-400" />
                       Send via Gmail
                       <ChevronDown size={14} />
                    </button>
                 </div>
              </div>

              <div className="text-[15px] text-gray-400 font-medium">
                 Here's a quick overview of what the research found, along with the email ready to send:
              </div>
           </div>
        </div>
     </div>

     <div style={{ padding: '24px 32px 48px' }}>
        <div className="max-w-3xl mx-auto bg-[#1e1e1e] border border-white/5 p-4 px-6 rounded-[2.5rem] flex items-center gap-4 shadow-2xl relative">
           <Plus className="w-5 h-5 text-gray-500 hover:text-white cursor-pointer" />
           <div className="flex-1 text-gray-500 text-sm">Reply...</div>
           <div className="flex items-center gap-4 text-gray-600">
              <div className="flex items-center gap-2 text-[11px] font-bold hover:bg-white/5 px-2 py-1 rounded cursor-pointer">
                 <span>Sonnet 4.7</span>
                 <ChevronDown size={12} />
              </div>
              <Volume2 className="w-4 h-4 cursor-pointer hover:text-white" />
           </div>
           
           <div className="absolute -bottom-8 left-0 right-0 text-center text-[10px] text-gray-600 font-medium">
              Claude is AI and can make mistakes. Please double-check responses.
           </div>
        </div>
     </div>
  </div>
);

// --- Main Page ---

export default function Home() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [handoffResult, setHandoffResult] = useState<any>(null);
  const [isHandingOff, setIsHandingOff] = useState(false);
  const [view, setView] = useState<'triage' | 'handoff'>('triage');
  const [error, setError] = useState<string | null>(null);

  const handleTriage = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setResult(null);
    setHandoffResult(null);
    setView('triage');

    try {
      const res = await fetch("/api/triage", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt }),
      });
      
      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.detail || "Failed to contact the orchestration engine.");
      }

      const data = await res.json();
      setResult(data);
      setError(null);
    } catch (err: any) {
      console.error("Triage failed:", err);
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  const handleHandoff = async () => {
    if (!result?.strategy) return;
    setIsHandingOff(true);
    
    try {
      const res = await fetch("/api/handoff", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          prompt, 
          strategy: result.strategy 
        }),
      });
      
      if (!res.ok) {
        throw new Error("Failed to establishment handoff context.");
      }

      const data = await res.json();
      setHandoffResult(data.handoff_bundle);
      setError(null);
    } catch (err: any) {
      console.error("Handoff failed:", err);
      setError(err.message || "Handoff connection lost.");
    } finally {
      setIsHandingOff(false);
    }
  };

  const handleNewChat = () => {
    setPrompt("");
    setResult(null);
    setLoading(false);
    setHandoffResult(null);
    setIsHandingOff(false);
    setView('triage');
    setError(null);
  };

  // The main layout now always includes the Sidebar for AI and Cowork views.
  // Claude Code remains a full-screen specialized environment.
  if (view === 'handoff' && handoffResult && handoffResult.target_environment === 'Claude Code') {
    return <ClaudeCodeSimulation bundle={handoffResult} onExit={() => setView('triage')} />;
  }

  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'hidden', backgroundColor: '#0d0d0d' }} className="text-white/50">
      <Sidebar 
        activePrompt={result ? prompt : undefined} 
        onNewChat={handleNewChat}
      />

      <main style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-start', paddingTop: view === 'handoff' ? '0' : '100px', position: 'relative', overflowY: 'auto', backgroundColor: '#111111', color: 'rgba(255,255,255,0.8)' }}>
        {view === 'handoff' && handoffResult ? (
          handoffResult.target_environment === 'Claude Cowork' ? (
            <ClaudeCoworkSimulation bundle={handoffResult} onExit={() => setView('triage')} />
          ) : (
            <ClaudeAIView bundle={handoffResult} onExit={() => setView('triage')} />
          )
        ) : (
          <>
            <div className="absolute top-8 right-8">
               <button className="px-4 py-1.5 bg-white/5 rounded-full border border-white/10 text-[11px] font-bold text-white hover:bg-white/10 transition-colors">Get Pro</button>
            </div>

            <AnimatePresence mode="wait">
              {!result ? (
                <motion.div 
                  key="home"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.98 }}
                  style={{ maxWidth: '768px', width: '100%', display: 'flex', flexDirection: 'column', gap: '40px', alignItems: 'center' }}
                >
                  <div className="flex flex-col items-center gap-6">
                     <div className="flex items-center gap-4 text-white/90">
                        <span className="text-[#d97757] text-4xl font-serif leading-none -mt-1">＊</span>
                        <h1 className="text-5xl font-serif font-medium tracking-tight">Back at it, User</h1>
                     </div>
                  </div>

                  <div className="w-full bg-[#1e1e1e] border border-white/5 rounded-[2.5rem] p-5 shadow-2xl relative transition-all group hover:border-white/10 focus-within:border-white/20">
                      <textarea
                        value={prompt}
                        onChange={(e) => setPrompt(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && !e.shiftKey && handleTriage()}
                        placeholder="How can I help you today?"
                        style={{ width: '100%', minHeight: '144px', backgroundColor: 'transparent', color: 'rgba(255,255,255,0.9)', outline: 'none', border: 'none', resize: 'none', fontSize: '20px', padding: '16px' }}
                      />
                     <div className="flex justify-between items-center px-4 pb-2">
                        <div className="flex gap-6 text-gray-500">
                           <Plus className="w-5 h-5 cursor-pointer hover:text-white transition-colors" />
                        </div>
                         <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2 text-xs font-bold text-gray-400 px-3 py-1.5 hover:bg-white/5 rounded-lg cursor-pointer transition-colors group/btn border border-white/5">
                               <span>Sonnet 4.7</span>
                               <ChevronDown className="w-3 h-3 opacity-60" />
                            </div>
                            <div className="w-8 h-8 rounded-full border border-white/10 flex items-center justify-center hover:bg-white/5 cursor-pointer transition-colors">
                               <Volume2 className="w-3.5 h-3.5 text-gray-400" />
                            </div>
                           <button
                             onClick={handleTriage}
                             disabled={loading || !prompt.trim()}
                             className={`w-10 h-10 rounded-xl flex items-center justify-center transition-all ${loading || !prompt.trim() ? 'bg-gray-800 text-gray-600' : 'bg-white/10 text-white/40 hover:bg-white/20 hover:text-white'}`}
                           >
                             {loading ? <div className="w-4 h-4 border-2 border-white/20 border-t-white/80 rounded-full animate-spin" /> : <ArrowRight className="w-5 h-5" />}
                           </button>
                        </div>
                     </div>
                  </div>

                  {error && (
                    <motion.div 
                      initial={{ opacity: 0, y: -10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="w-full max-w-xl p-4 px-6 bg-red-500/10 border border-red-500/20 rounded-2xl flex items-center gap-4 text-red-400 text-sm font-medium"
                    >
                      <div className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
                      {error}
                    </motion.div>
                  )}

                  <div className="flex flex-wrap justify-center gap-2.5 opacity-60">
                    <Tag icon={<CodeIcon size={12}/>} name="Code" />
                    <Tag icon={<Search size={12}/>} name="Learn" />
                    <Tag icon={<AlignLeft size={12}/>} name="Write" />
                    <Tag icon={<Layout size={12}/>} name="Life stuff" />
                    <Tag icon={<Sparkles size={12}/>} name="Claude's choice" />
                  </div>
                </motion.div>
              ) : (
                <motion.div 
                  key="result"
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="max-w-4xl w-full flex flex-col gap-10 pb-32"
                >
                   <div className="flex justify-end pr-4">
                      <div className="max-w-2xl bg-[#1e1e1e] p-6 rounded-[2.5rem] text-[15px] text-white/90 leading-relaxed shadow-xl">
                        {prompt}
                      </div>
                   </div>

                   <div className="bg-[#181818] border border-white/5 rounded-3xl overflow-hidden shadow-2xl relative">
                      <div className="bg-[#0f0f0f] border-b border-white/10 p-3.5 flex justify-between items-center px-8">
                         <div className="flex items-center gap-3">
                            <div className="w-5 h-5 bg-blue-500/10 rounded flex items-center justify-center">
                               <Layout size={12} className="text-blue-400" />
                            </div>
                            <span className="text-[11px] font-bold text-gray-500 tracking-[0.2em] uppercase">Strategy Artifact</span>
                         </div>
                         <div className="flex items-center gap-5 text-gray-600">
                            <ArrowRight size={14} className="cursor-pointer hover:text-white transition-colors" />
                            <Maximize2 size={14} className="cursor-pointer hover:text-white transition-colors" />
                         </div>
                      </div>

                      <div className="p-10 md:p-14 space-y-12 bg-gradient-to-b from-[#181818] to-[#121212]">
                         <div className="space-y-6 text-center border-b border-white/5 pb-14">
                            <h2 className="text-4xl font-serif text-white/90 tracking-tight italic leading-snug max-w-2xl mx-auto">
                               {result.intent === 'COMPLEX' ? "This request warrants a multi-agent orchestration strategy." : "This is a standard direct response task."}
                            </h2>
                            <div className="inline-flex items-center gap-3 px-4 py-1.5 bg-white/5 rounded-full text-[11px] text-gray-500 tracking-wider uppercase font-bold border border-white/5">
                               <span className="w-1.5 h-1.5 rounded-full bg-blue-400 animate-pulse"></span>
                               {result.intent} Severity • {result.classification.confidence * 100}% Confidence
                            </div>
                         </div>

                         {result.strategy && (
                            <div className="space-y-14">
                               <div className="space-y-10">
                                  <div className="flex items-center gap-4">
                                     <span className="text-[11px] font-bold text-gray-600 uppercase tracking-[0.3em] px-1">Serialized Steps</span>
                                     <div className="flex-1 h-[1px] bg-white/5"></div>
                                  </div>
                                  <div className="grid gap-4">
                                     {result.strategy.steps.map((step: any, idx: number) => (
                                        <div key={idx} className="flex gap-8 p-6 hover:bg-white/[0.02] rounded-[2rem] transition-all border border-transparent hover:border-white/5 group">
                                           <div className="flex flex-col items-center gap-4">
                                              <div className="w-8 h-8 rounded-full border border-white/5 flex items-center justify-center text-xs font-black text-gray-700 group-hover:text-blue-400 group-hover:border-blue-400/20 transition-all duration-500">0{idx + 1}</div>
                                              {idx < result.strategy.steps.length - 1 && <div className="w-[1px] flex-1 bg-white/5"></div>}
                                           </div>
                                           <div className="pt-0.5">
                                              <div className="text-lg font-bold text-white/90 tracking-tight">{step.title}</div>
                                              <div className="text-[15px] text-gray-500 mt-2 leading-relaxed font-medium">{step.description}</div>
                                           </div>
                                        </div>
                                     ))}
                                  </div>
                               </div>

                               <div className="grid grid-cols-1 md:grid-cols-3 gap-8 border-y border-white/5 py-10 px-4 mt-6">
                                  <div className="flex flex-col gap-2">
                                     <span className="text-[10px] text-gray-600 font-bold uppercase tracking-widest">Recommended Environment</span>
                                     <span className="text-[15px] font-bold text-blue-400 italic font-serif">{result.strategy.recommended_environment}</span>
                                  </div>
                                  <div className="flex flex-col gap-2 border-x border-white/5 px-8">
                                     <span className="text-[10px] text-gray-600 font-bold uppercase tracking-widest">Model Selection</span>
                                     <span className="text-[15px] font-bold text-white/90 uppercase tracking-tight">{result.strategy.recommended_model}</span>
                                  </div>
                                  <div className="flex flex-col gap-2">
                                     <span className="text-[10px] text-gray-600 font-bold uppercase tracking-widest">Estimated Total Time</span>
                                     <span className="text-[15px] font-bold text-white/90 uppercase tracking-tight">{result.strategy.estimated_total_time_mins} mins</span>
                                  </div>
                               </div>

                               <div className="flex justify-center pt-8">
                                 <button 
                                   onClick={handleHandoff}
                                   disabled={isHandingOff}
                                   className={`group relative overflow-hidden px-16 py-6 rounded-[2rem] font-bold text-lg flex items-center justify-center gap-5 transition-all shadow-[0_0_50px_rgba(0,0,0,0.5)] ${isHandingOff ? 'bg-gray-800 text-gray-500 cursor-not-allowed' : 'bg-white text-black hover:scale-[1.03] active:scale-95'}`}
                                 >
                                   <span className="relative z-10">{isHandingOff ? "PREPARING HANDOFF..." : `PROCEED TO ${result.strategy.recommended_environment.toUpperCase()}`}</span>
                                   <ArrowRight size={22} className="relative z-10 group-hover:translate-x-2 transition-transform duration-500" />
                                   <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                                 </button>
                               </div>
                            </div>
                         )}
                      </div>
                   </div>
                </motion.div>
              )}
            </AnimatePresence>

            {/* Floating Handoff Overlay (Native Style) */}
            <AnimatePresence>
              {handoffResult && (
                <motion.div 
                   initial={{ opacity: 0, scale: 0.95 }}
                   animate={{ opacity: 1, scale: 1 }}
                   exit={{ opacity: 0, scale: 1.05 }}
                   className="fixed inset-0 z-[200] flex items-center justify-center bg-black/80 backdrop-blur-sm p-4"
                >
                   <div className="max-w-xl w-full bg-[#1a1a1a] border border-white/10 rounded-[2.5rem] shadow-[0_0_100px_rgba(0,0,0,0.5)] p-12 text-center space-y-8">
                      <div className="w-20 h-20 bg-green-500/10 rounded-full flex items-center justify-center border border-green-500/30 mx-auto">
                        <CheckCircle className="w-10 h-10 text-green-500" />
                      </div>
                      <div className="space-y-4">
                         <h3 className="text-3xl font-serif text-white tracking-tight uppercase tracking-widest italic">Handoff Ready</h3>
                         <p className="text-gray-400 leading-relaxed italic">"Strategic context has been fully serialized. Establishing bridge to {handoffResult.target_environment}..."</p>
                      </div>
                      
                      <div className="flex flex-col gap-4">
                         <button 
                           onClick={() => setView('handoff')}
                           className="w-full py-4 bg-white text-black font-black rounded-xl hover:scale-105 transition-all text-sm uppercase tracking-widest"
                         >
                           Enter Environment
                         </button>
                         <button 
                           onClick={() => setHandoffResult(null)}
                           className="text-[10px] font-bold text-gray-500 hover:text-white transition-colors uppercase tracking-[0.3em]"
                         >
                           Review Plan Again
                         </button>
                      </div>
                   </div>
                </motion.div>
              )}
            </AnimatePresence>

            <div className="fixed bottom-8 text-[10px] text-gray-700 tracking-[0.5em] uppercase font-bold">
               Claude Orchestration Layer • Agentic Middleware
            </div>
          </>
        )}
      </main>
    </div>
  );
}
