import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import type { ExpenseOverTime } from '../../api/analytics';

interface Props {
    data: ExpenseOverTime[];
}

const ExpenseOverTimeChart: React.FC<Props> = ({ data }) => {
    const svgRef = useRef<SVGSVGElement>(null);

    useEffect(() => {
        if (!svgRef.current || data.length === 0) return;

        const margin = { top: 20, right: 30, bottom: 40, left: 60 };
        const width = 800 - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;

        const svg = d3.select(svgRef.current);
        svg.selectAll('*').remove();

        const g = svg
            .append('g')
            .attr('transform', `translate(${margin.left}, ${margin.top})`);

        const parseDate = d3.timeParse('%Y-%m-%d');
        const formattedData = data.map(d => ({
            date: parseDate(d.date) || new Date(),
            amount: d.amount
        })).sort((a, b) => a.date.getTime() - b.date.getTime());

        const x = d3.scaleTime()
            .domain(d3.extent(formattedData, d => d.date) as [Date, Date])
            .range([0, width]);

        const y = d3.scaleLinear()
            .domain([0, d3.max(formattedData, d => d.amount) || 0])
            .nice()
            .range([height, 0]);

        // Add X axis
        g.append('g')
            .attr('transform', `translate(0, ${height})`)
            .call(d3.axisBottom(x).ticks(width / 80).tickFormat(d3.timeFormat('%b %d') as any))
            .selectAll('text')
            .style('text-anchor', 'end')
            .attr('dx', '-.8em')
            .attr('dy', '.15em')
            .attr('transform', 'rotate(-45)');

        // Add Y axis
        g.append('g')
            .call(d3.axisLeft(y).ticks(5).tickFormat(d => `$${d}`));

        // Add line
        const line = d3.line<{ date: Date, amount: number }>()
            .x(d => x(d.date))
            .y(d => y(d.amount))
            .curve(d3.curveMonotoneX);

        g.append('path')
            .datum(formattedData)
            .attr('fill', 'none')
            .attr('stroke', '#4f46e5')
            .attr('stroke-width', 3)
            .attr('d', line);

        // Add area
        const area = d3.area<{ date: Date, amount: number }>()
            .x(d => x(d.date))
            .y0(height)
            .y1(d => y(d.amount))
            .curve(d3.curveMonotoneX);

        g.append('path')
            .datum(formattedData)
            .attr('fill', 'url(#area-gradient)')
            .attr('d', area);

        // Add gradient
        const gradient = svg.append('defs')
            .append('linearGradient')
            .attr('id', 'area-gradient')
            .attr('x1', '0%')
            .attr('y1', '0%')
            .attr('x2', '0%')
            .attr('y2', '100%');

        gradient.append('stop')
            .attr('offset', '0%')
            .attr('stop-color', '#4f46e5')
            .attr('stop-opacity', 0.3);

        gradient.append('stop')
            .attr('offset', '100%')
            .attr('stop-color', '#4f46e5')
            .attr('stop-opacity', 0);

        // Add dots
        g.selectAll('.dot')
            .data(formattedData)
            .enter()
            .append('circle')
            .attr('class', 'dot')
            .attr('cx', d => x(d.date))
            .attr('cy', d => y(d.amount))
            .attr('r', 4)
            .attr('fill', '#4f46e5')
            .attr('stroke', 'white')
            .attr('stroke-width', 2)
            .on('mouseover', function () {
                d3.select(this).attr('r', 6);
                // Tooltip could be added here
            })
            .on('mouseout', function () {
                d3.select(this).attr('r', 4);
            });

    }, [data]);

    return (
        <div className="w-full overflow-x-auto">
            <svg ref={svgRef} width={800} height={400}></svg>
        </div>
    );
};

export default ExpenseOverTimeChart;
