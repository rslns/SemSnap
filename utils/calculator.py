def calculate_sgpa(subjects, scale=10):
    """
    subjects: list of dicts with 'credits' and 'grade_point'
    scale: 10 or 4
    """
    total_credits = sum(s['credits'] for s in subjects)
    if total_credits == 0:
        return 0
    weighted_sum = sum(s['credits'] * s['grade_point'] for s in subjects)
    sgpa = weighted_sum / total_credits
    return round(sgpa, 2)


def calculate_cgpa(semesters):
    """
    semesters: list of dicts with 'sgpa' and 'credits'
    """
    total_credits = sum(s['credits'] for s in semesters)
    if total_credits == 0:
        return 0
    weighted_sum = sum(s['sgpa'] * s['credits'] for s in semesters)
    cgpa = weighted_sum / total_credits
    return round(cgpa, 2)


def suggest_sgpa(current_cgpa, completed_credits, target_cgpa, next_credits, scale=10):
    """
    Returns the SGPA needed next semester to reach target CGPA
    """
    total_credits = completed_credits + next_credits
    required_weighted = target_cgpa * total_credits
    current_weighted = current_cgpa * completed_credits
    needed = (required_weighted - current_weighted) / next_credits
    needed = round(needed, 2)
    if needed > scale:
        return None  # not achievable
    if needed < 0:
        return 0
    return needed


def convert_grade(value, from_type, scale=10):
    """
    from_type: 'percentage', 'grade_point', 'letter'
    Returns dict with all three formats
    """
    if scale == 10:
        grade_table = [
            (90, 100, 10, 'O'),
            (80, 89.99, 9, 'A+'),
            (70, 79.99, 8, 'A'),
            (60, 69.99, 7, 'B+'),
            (50, 59.99, 6, 'B'),
            (40, 49.99, 5, 'C'),
            (0,  39.99, 0, 'F'),
        ]
    else:
        grade_table = [
            (93, 100, 4.0, 'A'),
            (90, 92.99, 3.7, 'A-'),
            (87, 89.99, 3.3, 'B+'),
            (83, 86.99, 3.0, 'B'),
            (80, 82.99, 2.7, 'B-'),
            (77, 79.99, 2.3, 'C+'),
            (73, 76.99, 2.0, 'C'),
            (70, 72.99, 1.7, 'C-'),
            (67, 69.99, 1.3, 'D+'),
            (65, 66.99, 1.0, 'D'),
            (0,  64.99, 0.0, 'F'),
        ]

    if from_type == 'percentage':
        pct = float(value)
        for low, high, gp, letter in grade_table:
            if low <= pct <= high:
                return {'percentage': pct, 'grade_point': gp, 'letter': letter}

    elif from_type == 'grade_point':
        gp = float(value)
        for low, high, table_gp, letter in grade_table:
            if gp == table_gp:
                return {'percentage': (low + high) / 2, 'grade_point': gp, 'letter': letter}

    elif from_type == 'letter':
        for low, high, gp, letter in grade_table:
            if value.upper() == letter:
                return {'percentage': (low + high) / 2, 'grade_point': gp, 'letter': letter}

    return None
