#!/usr/bin/env python3
"""
Global Cultural Heritage Preservation Network
Author: Pranay M.

Platform that documents, preserves, and makes accessible
endangered languages, traditions, and knowledge.
"""

import ollama
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from rich.prompt import Prompt
import json
import sys

console = Console()

BANNER = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║           🏛️ GLOBAL CULTURAL HERITAGE PRESERVATION NETWORK 🏛️                  ║
║                    Endangered Knowledge Documentation System                   ║
║                           Author: Pranay M.                                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

MODULES = {
    "1": ("Language Documenter", "language_doc", "Document endangered languages"),
    "2": ("Tradition Recorder", "tradition", "Record cultural traditions"),
    "3": ("Knowledge Mapper", "knowledge_map", "Map traditional knowledge systems"),
    "4": ("Endangerment Assessor", "endangerment", "Assess cultural endangerment levels"),
    "5": ("Preservation Planner", "preservation", "Plan preservation strategies"),
    "6": ("Community Connector", "community", "Connect communities and resources"),
    "7": ("Digital Archive Designer", "archive", "Design digital preservation archives"),
    "8": ("Accessibility Manager", "accessibility", "Manage content accessibility"),
    "9": ("Revitalization Advisor", "revitalization", "Advise on cultural revitalization"),
    "10": ("Heritage Dashboard", "dashboard", "Generate heritage preservation dashboard")
}

SYSTEM_PROMPTS = {
    "language_doc": """You are an expert linguist specializing in language documentation.

For each language documentation, provide:

1. **Language Profile**: Name, classification, speakers, location, status
2. **Phonological System**: Sound inventory, patterns, transcription
3. **Grammatical Structure**: Morphology, syntax, unique features
4. **Lexicon**: Core vocabulary, specialized terms, etymology
5. **Oral Literature**: Stories, songs, proverbs, oral traditions
6. **Documentation Plan**: Recording priorities, methods, timeline

Document endangered languages comprehensively.""",

    "tradition": """You are an expert ethnographer and cultural documentation specialist.

For each tradition recording, document:

1. **Tradition Overview**: Name, type, community, significance
2. **Historical Context**: Origins, evolution, influences
3. **Practice Details**: How performed, when, by whom, materials
4. **Knowledge Holders**: Who knows, transmission methods
5. **Current Status**: Active, declining, adapted, at risk
6. **Recording Strategy**: Best methods, ethical considerations

Record cultural traditions thoroughly.""",

    "knowledge_map": """You are an expert in traditional knowledge systems.

For each knowledge mapping, analyze:

1. **Knowledge Domain**: Area (medicine, agriculture, crafts, etc.)
2. **Knowledge Content**: Specific knowledge, techniques, materials
3. **Knowledge Structure**: Organization, categories, relationships
4. **Transmission**: How taught and learned, apprenticeship
5. **Integration**: Links to other knowledge, worldview connections
6. **Preservation Needs**: What's at risk, priority elements

Map traditional knowledge systems comprehensively.""",

    "endangerment": """You are an expert in cultural vitality assessment.

For each endangerment assessment, evaluate:

1. **Vitality Indicators**: Active use, intergenerational transmission
2. **Speaker/Practitioner Numbers**: Quantity, age distribution, trends
3. **Domain Usage**: Where culture is used, functional load
4. **Attitude Assessment**: Community and external attitudes
5. **Threat Analysis**: Factors causing decline, severity
6. **Urgency Rating**: Critical, severely endangered, vulnerable, safe

Assess cultural endangerment levels accurately.""",

    "preservation": """You are an expert in cultural preservation strategy.

For each preservation plan, develop:

1. **Preservation Goals**: What to preserve, success criteria
2. **Method Selection**: Documentation, archiving, revitalization
3. **Community Engagement**: Involvement, consent, benefit sharing
4. **Resource Requirements**: Funding, technology, expertise
5. **Implementation Timeline**: Phases, milestones, responsibilities
6. **Sustainability**: Long-term maintenance, access, updating

Plan effective preservation strategies.""",

    "community": """You are an expert in heritage community engagement.

For each community connection, facilitate:

1. **Community Identification**: Who to engage, stakeholders
2. **Needs Assessment**: Community priorities, concerns
3. **Resource Matching**: Available support, partnerships
4. **Capacity Building**: Training, tools, empowerment
5. **Collaboration Models**: Partnership structures, agreements
6. **Benefit Sharing**: How community benefits, ownership

Connect communities with preservation resources.""",

    "archive": """You are an expert in digital preservation and archiving.

For each archive design, specify:

1. **Content Types**: Audio, video, text, images, 3D
2. **Metadata Standards**: Description, organization, search
3. **Storage Architecture**: Format, redundancy, migration
4. **Access Controls**: Who can access, permissions levels
5. **Interface Design**: How users interact, search, browse
6. **Sustainability**: Long-term maintenance, funding, governance

Design effective digital archives.""",

    "accessibility": """You are an expert in cultural content accessibility.

For each accessibility request, address:

1. **Target Audiences**: Who should access, their needs
2. **Access Barriers**: Technical, linguistic, cultural barriers
3. **Format Adaptations**: Translations, formats, interfaces
4. **Ethical Access**: Appropriate sharing, sacred materials
5. **Distribution Channels**: How to reach audiences
6. **Feedback Integration**: User input, continuous improvement

Manage cultural content accessibility.""",

    "revitalization": """You are an expert in cultural and language revitalization.

For each revitalization advice, provide:

1. **Situation Analysis**: Current state, resources, opportunities
2. **Revitalization Approaches**: Immersion, education, media, events
3. **Success Factors**: What enables successful revitalization
4. **Community Mobilization**: Engaging speakers, youth, leaders
5. **Resource Development**: Materials, programs, spaces
6. **Long-term Strategy**: Sustainability, growth, integration

Advise on cultural revitalization strategies.""",

    "dashboard": """You are an expert in heritage preservation analytics.

For each dashboard, generate:

1. **Global Overview**: Languages/traditions at risk, trends
2. **Documentation Status**: Coverage, gaps, priorities
3. **Community Engagement**: Active projects, partnerships
4. **Resource Allocation**: Funding, expertise distribution
5. **Success Stories**: Revitalization wins, best practices
6. **Urgent Actions**: Critical situations, immediate needs

Generate heritage preservation dashboards."""
}

def get_multiline_input(prompt_text):
    console.print(f"\n[cyan]{prompt_text}[/cyan]")
    console.print("[dim](Type 'END' on a new line when finished)[/dim]\n")
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END':
                break
            lines.append(line)
        except EOFError:
            break
    return '\n'.join(lines)

def query_llama(system_prompt, user_input):
    try:
        response = ollama.chat(model='llama3.2', messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_input}
        ])
        return response['message']['content']
    except Exception as e:
        return f"Error: {str(e)}\n\nMake sure Ollama is running."

def display_menu():
    console.print(BANNER, style="bold blue")
    table = Table(title="🏛️ Heritage Modules", show_header=True, header_style="bold magenta")
    table.add_column("Option", style="cyan", width=8)
    table.add_column("Module", style="green", width=28)
    table.add_column("Description", style="white", width=42)
    for key, (name, _, desc) in MODULES.items():
        table.add_row(key, name, desc)
    table.add_row("0", "Exit", "Exit the application")
    console.print(table)

def run_module(module_key):
    name, key, desc = MODULES[module_key]
    console.print(Panel(f"🏛️ {name}", style="bold green"))
    user_input = get_multiline_input(f"Describe your {name.lower()} request:")
    with console.status(f"[bold green]Processing {name}..."):
        response = query_llama(SYSTEM_PROMPTS[key], user_input)
    console.print(Panel(Markdown(response), title=f"🏛️ {name} Results", border_style="green"))

def main():
    while True:
        display_menu()
        choice = Prompt.ask("\nSelect a module", choices=["0","1","2","3","4","5","6","7","8","9","10"])
        if choice == "0":
            console.print("\n[yellow]Thank you for using the Cultural Heritage Preservation Network![/yellow]")
            console.print("[dim]Author: Pranay M.[/dim]\n")
            break
        try:
            run_module(choice)
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled.[/yellow]")
        except Exception as e:
            console.print(f"\n[red]Error: {str(e)}[/red]")
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
