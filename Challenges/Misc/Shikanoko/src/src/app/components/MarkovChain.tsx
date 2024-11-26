"use client";

import React, { useEffect, useState, useRef, use } from "react";
import * as d3 from "d3";
import "./MarkovChain.css";

export class FSMState {
    id: string;
    label: string;
    duration: number;
    start: number;
    end: number;
    x: number;
    y: number;

    constructor(id: string, label: string, start: number, end: number, x: number, y: number) {
        this.id = id;
        this.label = label;
        this.duration = end - start;
        this.start = start;
        this.end = end;
        this.x = x;
        this.y = y;
    }
}

export class FSMEdge {
    source: string;
    target: string;
    probability: number;

    constructor(source: string, target: string, probability: number) {
        this.source = source;
        this.target = target;
        this.probability = probability;
    }
}

export default function MarkovChain({
    states,
    links,
    width = 800,
    height = 400,
    setSeek,
    isRunning
} : {
    states: FSMState[],
    links: FSMEdge[],
    width?: number,
    height?: number,
    setSeek: (time: number) => void,
    isRunning: boolean
})
{
    const svgRef = useRef<SVGSVGElement>(null);
    const currentStateRef = useRef<FSMState>(states[0]);
    let history = ''

    const drawQuadraticCurve = (x1: number, y1: number, x2: number, y2: number) => {
        const theta = Math.atan2(y2 - y1, x2 - x1);
        const h = -50;
        const xf = (x1 + x2) / 2 + h * Math.cos(theta + Math.PI / 2);
        const yf = (y1 + y2) / 2 + h * Math.sin(theta + Math.PI / 2);
        return `M${x1} ${y1} Q${xf} ${yf}, ${x2} ${y2}`;
    };

    const drawBezierCurve = (x: number, y: number) => {
        const d = y > height / 2 ? 100 : -100;
        return `M${x} ${y} C${x + d} ${y + d}, ${x - d} ${y + d}, ${x} ${y}`;
    }

    const getNextState = (currentState: FSMState) => {
        const next = links.filter(link => link.source === currentState.id);
        const random = Math.random();
        let sum = 0;
        for (let i = 0; i < next.length; i++) {
            sum += next[i].probability;
            if (random < sum) {
                return states.find(state => state.id === next[i].target);
            }
        }
        return currentState;
    };

    const timeout = useRef<NodeJS.Timeout | null>(null);
    const transition = () => {
        if(timeout.current)
            clearTimeout(timeout.current);
        const next = getNextState(currentStateRef.current) ?? states[3];
        // console.log(`curr: ${currentStateRef.current.id}, next: ${next.id}`);
        d3.select(`#node_${currentStateRef.current.id}`).classed("current-node", false);
        d3.select(`#node_${next.id}`).classed("current-node", true);
        setState(next)
        setSeek(currentStateRef.current.start);
        timeout.current = setTimeout(transition, currentStateRef.current.duration * 1000);
    }
    
    let [requirement, setRequirement] = useState('しかのこのこのここしたんたん'+'しかのこのこのここしたんたん')    

    let flagraw = 'PdKox67RmJLxO+9z1QR'

    const setState = (next: FSMState) => {
        currentStateRef.current = next;
        history += next.label
        
        if (history.substring(history.length-requirement.length) == requirement) {
            flagraw += 'vfsIvJIafDT8r9bURn'
            win()
        }
    }



    const win = () => {
        // I pray this is sufficient obfuscation
        const filter = (e: string) =>  {
            return e[0].charCodeAt(0) == 0o141 && e[4] && !e[5]
        }

        const filter2 = (e: string) => {
            return e[0].charCodeAt(0) == 0o141 && !e[4] && !e[5]
        }

        function RC4(key: string, input: string) {
            const S = [];
            let j = 0;
            let i = 0;
            let x;
        
            // KSA (Key Scheduling Algorithm)
            for (i = 0; i < 256; i++) {
                S[i] = i;
            }
        
            for (i = 0; i < 256; i++) {
                j = (j + S[i] + key.charCodeAt(i % key.length)) % 256;
                [S[i], S[j]] = [S[j], S[i]]; // Swap S[i] and S[j]
            }
        
            i = 0;
            j = 0;
            const result = [];
        
            // PRGA (Pseudo-Random Generation Algorithm)
            for (let y = 0; y < input.length; y++) {
                i = (i + 1) % 256;
                j = (j + S[i]) % 256;
                [S[i], S[j]] = [S[j], S[i]]; // Swap S[i] and S[j]
        
                x = S[(S[i] + S[j]) % 256];
                result.push(String.fromCharCode(input.charCodeAt(y) ^ x));
            }
        
            return result.join('');
        }

        flagraw += 'd89Pz/glFHQsz0/Mg=='
        // console.log(flagraw)
        // @ts-ignore
        let result = RC4('@ts-ignore', window[Object.keys(window).find(filter2)](flagraw))
        let g = RC4(result, 'gruh')
        // @ts-ignore
        window[Object.keys(window).find(filter)](window[Object.keys(window).find(filter2)](result))
    }

    useEffect(() => {
        const svg = d3.select(svgRef.current)
            .attr("width", width)
            .attr("height", height);

        // marker for arrowhead
        svg.append("defs").append("marker")
            .attr("id", "arrowhead")
            .attr("viewBox", "-0 -5 10 10")
            .attr("refX", 13)
            .attr("refY", 0)
            .attr("orient", "auto")
            .attr("markerWidth", 13)
            .attr("markerHeight", 13)
            .attr("xoverflow", "visible")
            .append("svg:path")
            .attr("d", "M 0,-5 L 6,0 L 0,5")
            .attr("fill", "#999")
            .style("stroke", "none");
        
        // edges
        const edge = svg.append("g")
            .attr("class", "edges")
            .selectAll("path")
            .data(links)
            .enter().append("path")
            .attr("class", "edge")
            .attr("marker-end", "url(#arrowhead)")
            .attr("d", (d) => {
                const source = states.find(state => state.id === d.source);
                const target = states.find(state => state.id === d.target);
                if(!source || !target) return "";
                if(source.x === target.x && source.y === target.y) {
                    return drawBezierCurve(source.x, source.y);
                }
                return drawQuadraticCurve(source.x, source.y, target.x, target.y);
            });
        
        // probability labels
        const edgeLabel = svg.append("g")
            .attr("class", "edge-labels")
            .selectAll("text")
            .data(links)
            .enter().append("text")
            .attr("x", d => {
                const source = states.find(state => state.id === d.source);
                const target = states.find(state => state.id === d.target);
                if(!source || !target) return 0;
                return (source.x + target.x) / 2;
            })
            .attr("y", d => {
                const source = states.find(state => state.id === d.source);
                const target = states.find(state => state.id === d.target);
                if(!source || !target) return 0;
                let dy = 0;
                if(source.x === target.x && source.y === target.y)
                {
                    if(source.y > height / 2)
                    {
                        dy = 90;
                    }
                    else
                    {
                        dy = -90;
                    }
                }
                else if(source.x > target.x)
                {
                    dy = 45;
                }
                else
                {
                    dy = -45;
                }
                return (source.y + target.y) / 2 + dy;
            })
            .text((d) => {
                if(d.probability == 1) return 1;
                if(d.probability == 0.5) return '½';
                return '¼';
            })

        // states
        const node = svg.append("g")
            .attr("class", "nodes")
            .selectAll("circle")
            .data(states)
            .enter().append("circle")
            .attr("id", d => `node_${d.id}`)
            .attr("class", "node")
            .attr("r", 20)
            .attr("cx", d => d.x)
            .attr("cy", d => d.y)
            .on("click", (event, d) => {
                if(timeout.current)
                    clearTimeout(timeout.current);
                d3.select(`#node_${currentStateRef.current.id}`).classed("current-node", false);
                d3.select(`#node_${currentStateRef.current.id}`).classed("current-node", true);
                setState(d)
                setSeek(currentStateRef.current.start);
                timeout.current = setTimeout(transition, currentStateRef.current.duration * 1000);
            });
        
        // state labels
        const label = svg.append("g")
            .attr("class", "labels")
            .selectAll("text")
            .data(states)
            .enter().append("text")
            .attr("class", "label")
            .attr("x", d => d.x)
            .attr("y", d => d.y)
            .text(d => d.label);
        
        d3.select(`#node_shi`).classed("current-node", true);

        timeout.current = setTimeout(transition, currentStateRef.current.duration * 1000);
    }, []);

    useEffect(() => {
        if(isRunning)
        {
            setTimeout(transition, currentStateRef.current.duration * 1000);
        }
        else
        {
            if(timeout.current)
                clearTimeout(timeout.current);
        }
    }, [isRunning]);

    return <svg ref={svgRef}></svg>;
}