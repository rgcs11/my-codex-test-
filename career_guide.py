#!/usr/bin/env python3
"""
Career Guide - Apna Career Path Explore Karo
Yeh tool aapko sahi career choose karne mein madad karega
"""

import os
import sys
from careers_data import CAREERS, INTERVIEW_TIPS, RESUME_TIPS, SKILL_DEVELOPMENT


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_divider(char="=", length=60):
    print(char * length)


def print_header():
    clear_screen()
    print_divider()
    print("        CAREER GUIDE - APNA FUTURE BANAO")
    print("     Sahi Career Choose Karne Ka Smart Tarika")
    print_divider()
    print()


def print_menu():
    print("MAIN MENU")
    print_divider("-")
    print("1. Career Options Explore Karo")
    print("2. Career Details Dekho")
    print("3. Interview Tips")
    print("4. Resume Tips")
    print("5. Skill Development Resources")
    print("6. Career Quiz - Mujhe Kaun Sa Career Sahi Hai?")
    print("7. Salary Comparison")
    print("0. Bahar Niklo")
    print_divider("-")


def list_careers():
    print_header()
    print("AVAILABLE CAREER OPTIONS")
    print_divider("-")
    for i, (key, career) in enumerate(CAREERS.items(), 1):
        print(f"{i}. {career['title']}")
    print_divider("-")


def show_career_detail(career_key):
    career = CAREERS[career_key]
    print_header()
    print(f"CAREER: {career['title']}")
    print_divider()

    print(f"\nDESCRIPTION:")
    print(f"  {career['description']}")

    print(f"\nZARURI SKILLS:")
    for skill in career['skills']:
        print(f"  - {skill}")

    print(f"\nEDUCATION PATH:")
    for edu in career['education']:
        print(f"  * {edu}")

    print(f"\nSALARY RANGE (India):")
    salary = career['salary_range']
    print(f"  Fresher:    {salary['fresher']}")
    print(f"  Mid-Level:  {salary['mid_level']}")
    print(f"  Senior:     {salary['senior']}")

    print(f"\nTOP COMPANIES:")
    print(f"  {', '.join(career['top_companies'])}")

    print(f"\nUSEFUL CERTIFICATIONS:")
    for cert in career['certifications']:
        print(f"  - {cert}")

    print(f"\nROADMAP - Kaise Shuru Karo:")
    for step in career['roadmap']:
        print(f"  {step}")

    print_divider()


def show_interview_tips():
    print_header()
    print("INTERVIEW TIPS - Interview Crack Karo!")
    print_divider("-")
    for i, tip in enumerate(INTERVIEW_TIPS, 1):
        print(f"{i:2}. {tip}")
    print_divider("-")


def show_resume_tips():
    print_header()
    print("RESUME TIPS - Behtareen Resume Banao!")
    print_divider("-")
    for i, tip in enumerate(RESUME_TIPS, 1):
        print(f"{i:2}. {tip}")
    print_divider("-")


def show_skill_development():
    print_header()
    print("SKILL DEVELOPMENT RESOURCES")
    print_divider()

    print("\nTECHNICAL SKILLS:")
    print_divider("-")
    for tip in SKILL_DEVELOPMENT['technical']:
        print(f"  -> {tip}")

    print("\nSOFT SKILLS:")
    print_divider("-")
    for tip in SKILL_DEVELOPMENT['soft_skills']:
        print(f"  -> {tip}")

    print("\nFREE LEARNING RESOURCES:")
    print_divider("-")
    for resource in SKILL_DEVELOPMENT['free_resources']:
        print(f"  * {resource}")
    print_divider()


def career_quiz():
    print_header()
    print("CAREER QUIZ - Apna Sahi Career Dhundho!")
    print_divider()
    print("Kuch simple sawaal poochhenge. Seedha jawab do.")
    print()

    scores = {key: 0 for key in CAREERS.keys()}

    questions = [
        {
            "question": "Aapko kaun sa kaam zyada pasand hai?",
            "options": [
                ("a", "Computer/Technology ke saath kaam karna", ["software_engineer", "data_scientist"]),
                ("b", "Logo ki madad karna (patients, clients)", ["doctor", "lawyer"]),
                ("c", "Numbers aur finance handle karna", ["ca"]),
                ("d", "Creative cheezein banana (design, art)", ["graphic_designer"]),
                ("e", "Desh ki seva karna aur administration", ["ias"]),
            ]
        },
        {
            "question": "Aap kitne saal padhai karne ke liye ready hain?",
            "options": [
                ("a", "2-3 saal (fast track career)", ["software_engineer", "graphic_designer"]),
                ("b", "4-5 saal (standard degree)", ["data_scientist", "ca", "lawyer"]),
                ("c", "6+ saal (long-term investment)", ["doctor", "ias"]),
            ]
        },
        {
            "question": "Aapki sabse badi strength kya hai?",
            "options": [
                ("a", "Logical thinking aur problem solving", ["software_engineer", "data_scientist"]),
                ("b", "Persuasion aur communication", ["lawyer", "ias"]),
                ("c", "Detail-oriented aur precise kaam", ["ca", "doctor"]),
                ("d", "Visual creativity aur aesthetics", ["graphic_designer"]),
            ]
        },
        {
            "question": "Kitni salary expect karte ho 5 saal baad?",
            "options": [
                ("a", "15-30 LPA (decent growth)", ["graphic_designer", "lawyer"]),
                ("b", "20-50 LPA (high growth)", ["software_engineer", "data_scientist", "ca"]),
                ("c", "Government salary + perks (stable life)", ["ias"]),
                ("d", "Koi limit nahi (own practice/consulting)", ["doctor", "lawyer", "ca"]),
            ]
        }
    ]

    for q_num, q in enumerate(questions, 1):
        print(f"Q{q_num}: {q['question']}")
        for opt_key, opt_text, _ in q['options']:
            print(f"  {opt_key}) {opt_text}")

        while True:
            choice = input("\nAapka jawab (letter): ").strip().lower()
            matched = [(k, t, careers) for k, t, careers in q['options'] if k == choice]
            if matched:
                _, _, matching_careers = matched[0]
                for career_key in matching_careers:
                    scores[career_key] += 1
                break
            else:
                print("Galat option! Dobara try karo.")
        print()

    sorted_careers = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    print_divider()
    print("QUIZ RESULTS - Aapke Liye Best Careers:")
    print_divider("-")
    for i, (career_key, score) in enumerate(sorted_careers[:3], 1):
        if score > 0:
            career_name = CAREERS[career_key]['title']
            bar = "#" * (score * 5)
            print(f"{i}. {career_name}")
            print(f"   Match: {bar} ({score}/4 points)")
    print_divider()


def salary_comparison():
    print_header()
    print("SALARY COMPARISON - India Mein Top Careers")
    print_divider()
    print(f"{'Career':<25} {'Fresher':<15} {'Mid-Level':<15} {'Senior':<20}")
    print_divider("-")

    for key, career in CAREERS.items():
        salary = career['salary_range']
        print(f"{career['title']:<25} {salary['fresher']:<15} {salary['mid_level']:<15} {salary['senior']:<20}")

    print_divider()
    print("NOTE: Salary depend karti hai location, company aur skills par")
    print_divider()


def select_career_menu():
    list_careers()
    career_keys = list(CAREERS.keys())

    print("Career number enter karo detail dekhne ke liye (0 = wapas):")
    while True:
        try:
            choice = int(input("Choice: "))
            if choice == 0:
                return
            elif 1 <= choice <= len(career_keys):
                show_career_detail(career_keys[choice - 1])
                input("\nEnter dabao continue karne ke liye...")
                return
            else:
                print(f"1 se {len(career_keys)} ke beech number enter karo!")
        except ValueError:
            print("Sirf number enter karo!")


def main():
    print_header()
    print("Career Guide mein aapka swagat hai!")
    print("Yeh tool aapko sahi career choose karne mein madad karega.")
    input("\nEnter dabao shuru karne ke liye...")

    while True:
        print_header()
        print_menu()

        choice = input("Apna choice enter karo: ").strip()

        if choice == "1":
            select_career_menu()
        elif choice == "2":
            select_career_menu()
        elif choice == "3":
            show_interview_tips()
            input("\nEnter dabao continue karne ke liye...")
        elif choice == "4":
            show_resume_tips()
            input("\nEnter dabao continue karne ke liye...")
        elif choice == "5":
            show_skill_development()
            input("\nEnter dabao continue karne ke liye...")
        elif choice == "6":
            career_quiz()
            input("\nEnter dabao continue karne ke liye...")
        elif choice == "7":
            salary_comparison()
            input("\nEnter dabao continue karne ke liye...")
        elif choice == "0":
            print_header()
            print("Dhanyawad! Apna career banao aur sफलता प्राप्त karo!")
            print_divider()
            sys.exit(0)
        else:
            print("Galat choice! 0-7 ke beech number enter karo.")
            input("Enter dabao continue karne ke liye...")


if __name__ == "__main__":
    main()
