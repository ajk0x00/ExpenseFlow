import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import type { ExpenseByCategory } from '../../api/analytics';

interface Props {
    data: ExpenseByCategory[];
}

const ExpenseByCategoryChart: React.FC<Props> = ({ data }) => {
    const svgRef = useRef<SVGSVGElement>(null);

    useEffect(() => {
        if (!svgRef.current || data.length === 0) return;

        const width = 400;
        const height = 400;
        const margin = 40;
        const radius = Math.min(width, height) / 2 - margin;

        const svg = d3.select(svgRef.current);
        svg.selectAll('*').remove();

        const g = svg
            .append('g')
            .attr('transform', `translate(${width / 2}, ${height / 2})`);

        const color = d3.scaleOrdinal<string>()
            .domain(data.map(d => d.category_name))
            .range(d3.schemeTableau10);

        const pie = d3.pie<ExpenseByCategory>()
            .value(d => d.amount)
            .sort(null);

        const arc = d3.arc<d3.PieArcDatum<ExpenseByCategory>>()
            .innerRadius(radius * 0.5)
            .outerRadius(radius);

        const labelArc = d3.arc<d3.PieArcDatum<ExpenseByCategory>>()
            .innerRadius(radius * 0.7)
            .outerRadius(radius * 0.7);

        const arcs = g.selectAll('.arc')
            .data(pie(data))
            .enter()
            .append('g')
            .attr('class', 'arc');

        arcs.append('path')
            .attr('d', arc)
            .attr('fill', d => color(d.data.category_name))
            .attr('stroke', 'white')
            .style('stroke-width', '2px')
            .style('opacity', 0.8)
            .on('mouseover', function () {
                d3.select(this).style('opacity', 1);
            })
            .on('mouseout', function () {
                d3.select(this).style('opacity', 0.8);
            });

        arcs.append('text')
            .attr('transform', d => `translate(${labelArc.centroid(d)})`)
            .attr('dy', '.35em')
            .style('text-anchor', 'middle')
            .style('font-size', '12px')
            .style('font-weight', 'bold')
            .style('fill', '#333')
            .text(d => d.data.percentage > 5 ? d.data.category_name : '');

    }, [data]);

    return (
        <div className="flex flex-col items-center">
            <svg ref={svgRef} width={400} height={400}></svg>
            <div className="mt-4 grid grid-cols-2 gap-2">
                {data.map((d, i) => (
                    <div key={i} className="flex items-center space-x-2">
                        <div
                            className="w-3 h-3 rounded-full"
                            style={{ backgroundColor: d3.schemeTableau10[i % 10] }}
                        ></div>
                        <span className="text-sm text-gray-600">{d.category_name}: {d.percentage}%</span>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ExpenseByCategoryChart;
