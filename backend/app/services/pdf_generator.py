"""
PDF Generator for Recipes
Creates formatted PDFs with reportlab
"""
from io import BytesIO
from typing import Dict, List
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


class RecipePDFGenerator:
    """Generator for Recipe PDFs"""

    def __init__(self):
        self.pagesize = A4
        self.margin = 2 * cm

    def generate(self, recipe_data: Dict) -> BytesIO:
        """
        Generate PDF for a recipe

        Args:
            recipe_data: Dict with recipe info
            {
                "name": str,
                "description": str,
                "difficulty": int,
                "cooking_time": str,
                "method": str,
                "servings": int,
                "ingredients": List[{"name": str, "amount": str, "carbs": float}],
                "nutrition_per_serving": {"calories": int, "protein": float, "carbs": float, "fat": float, "ke": float, "be": float}
            }

        Returns:
            BytesIO buffer with PDF
        """
        buffer = BytesIO()

        # Create PDF Document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=self.pagesize,
            leftMargin=self.margin,
            rightMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )

        # Styles
        styles = getSampleStyleSheet()

        # Custom Styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=20,
            alignment=TA_CENTER
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=16
        )

        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['Normal'],
            fontSize=11,
            leading=14
        )

        # Story (Content)
        story = []

        # 1. TITLE
        story.append(Paragraph(self._escape(recipe_data.get('name', 'Recipe')), title_style))
        story.append(Spacer(1, 0.5*cm))

        # 2. DESCRIPTION (if available)
        if recipe_data.get('description'):
            story.append(Paragraph(self._escape(recipe_data['description']), body_style))
            story.append(Spacer(1, 0.5*cm))

        # 3. META INFO TABLE
        difficulty = recipe_data.get('difficulty', 1)
        difficulty_text = '*' * difficulty

        meta_data = [
            ['Difficulty:', difficulty_text],
            ['Cooking Time:', str(recipe_data.get('cooking_time', '-'))],
            ['Method:', str(recipe_data.get('method', '-'))],
            ['Servings:', str(recipe_data.get('servings', 2))]
        ]

        meta_table = Table(meta_data, colWidths=[4*cm, 10*cm])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))

        story.append(meta_table)
        story.append(Spacer(1, 0.8*cm))

        # 4. INGREDIENTS
        story.append(Paragraph('Ingredients', heading_style))

        ingredients = recipe_data.get('ingredients', [])
        if ingredients:
            ingredients_data = [['Ingredient', 'Amount', 'Carbs (g)']]

            for ing in ingredients:
                carbs_val = ing.get('carbs', 0)
                carbs_str = f"{carbs_val:.1f}" if carbs_val else '-'
                ingredients_data.append([
                    self._escape(ing.get('name', '')),
                    self._escape(ing.get('amount', '')),
                    carbs_str
                ])

            ingredients_table = Table(ingredients_data, colWidths=[7*cm, 4*cm, 3*cm])
            ingredients_table.setStyle(TableStyle([
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 0), (-1, 0), 10),

                # Body
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#2c3e50')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('TOPPADDING', (0, 1), (-1, -1), 6),

                # Grid
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

                # Alternating rows
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')])
            ]))

            story.append(ingredients_table)
        else:
            story.append(Paragraph('No ingredients listed.', body_style))

        story.append(Spacer(1, 0.8*cm))

        # 5. NUTRITION PER SERVING
        nutrition = recipe_data.get('nutrition_per_serving', {})
        if nutrition:
            story.append(Paragraph('Nutrition per Serving', heading_style))

            nutrition_data = []

            if nutrition.get('calories'):
                nutrition_data.append(['Calories', f"{nutrition['calories']} kcal"])
            if nutrition.get('protein'):
                nutrition_data.append(['Protein', f"{nutrition['protein']:.1f} g"])
            if nutrition.get('carbs'):
                nutrition_data.append(['Carbohydrates', f"{nutrition['carbs']:.1f} g"])
            if nutrition.get('fat'):
                nutrition_data.append(['Fat', f"{nutrition['fat']:.1f} g"])

            # KE or BE (not both!)
            if nutrition.get('ke'):
                nutrition_data.append(['KE (Carb Units)', f"{nutrition['ke']:.1f}"])
            elif nutrition.get('be'):
                nutrition_data.append(['BE (Bread Units)', f"{nutrition['be']:.1f}"])

            if nutrition_data:
                nutrition_table = Table(nutrition_data, colWidths=[10*cm, 4*cm])
                nutrition_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 11),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
                ]))

                story.append(nutrition_table)

        # 6. FOOTER
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_CENTER
        )

        story.append(Spacer(1, 2*cm))
        story.append(Paragraph('Created with KitchenHelper-AI', footer_style))

        # Build PDF
        doc.build(story)

        # Reset buffer position
        buffer.seek(0)
        return buffer

    def _escape(self, text: str) -> str:
        """Escape special characters for reportlab"""
        if not text:
            return ''
        # Replace special chars that break reportlab
        return str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# Singleton Instance
pdf_generator = RecipePDFGenerator()
