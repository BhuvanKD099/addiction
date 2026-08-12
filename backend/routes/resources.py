from flask import Blueprint, jsonify, request
from utils.database import mysql

resources_bp = Blueprint("resources", __name__)

# Sample full-text resource content repository
RESOURCE_DETAILS = {
    1: {
        "resource_id": 1,
        "category": "Coping Techniques",
        "title": "10 Grounding Exercises for Intense Cravings",
        "content_type": "ARTICLE",
        "read_time": "5 Min Read",
        "description": "Learn the 5-4-3-2-1 sensory technique to navigate intense craving waves without yielding.",
        "full_content": """
        <h4>The 5-4-3-2-1 Coping & Grounding Technique</h4>
        <p class="text-muted">When a sudden craving strike occurs, your sympathetic nervous system triggers heightened distress. Grounding exercises redirect neurological focus back to the physical environment, lowering acute anxiety within 90 seconds.</p>
        
        <div class="p-3 bg-light rounded border mb-3">
            <h6 class="fw-bold text-primary"><i class="bi bi-eye-fill me-2"></i>5 Things You Can SEE</h6>
            <p class="small mb-0">Look around your room. Name 5 specific items out loud (e.g., a clock, a wooden table, a blue pen, light reflection, a leaf outside).</p>
        </div>

        <div class="p-3 bg-light rounded border mb-3">
            <h6 class="fw-bold text-success"><i class="bi bi-hand-index-fill me-2"></i>4 Things You Can TOUCH</h6>
            <p class="small mb-0">Notice physical sensations around you. Feel the texture of your shirt, cold water on your hands, the solid floor beneath your feet, or a smooth desk surface.</p>
        </div>

        <div class="p-3 bg-light rounded border mb-3">
            <h6 class="fw-bold text-warning"><i class="bi bi-ear-fill me-2"></i>3 Things You Can HEAR</h6>
            <p class="small mb-0">Listen closely to background acoustics. Identify 3 distinct sounds: ceiling fan hum, distant traffic, or bird chirping.</p>
        </div>

        <div class="p-3 bg-light rounded border mb-3">
            <h6 class="fw-bold text-danger"><i class="bi bi-wind me-2"></i>2 Things You Can SMELL</h6>
            <p class="small mb-0">Inhale deeply. Notice subtle scents like fresh coffee, soap, essential oils, or crisp outdoor air.</p>
        </div>

        <div class="p-3 bg-light rounded border mb-3">
            <h6 class="fw-bold text-info"><i class="bi bi-cup-hot-fill me-2"></i>1 Thing You Can TASTE</h6>
            <p class="small mb-0">Focus on the current taste in your mouth, or take a sip of cool mint tea or lemon water.</p>
        </div>
        """
    },
    2: {
        "resource_id": 2,
        "category": "Mindfulness & Meditation",
        "title": "Guided Morning Recovery Breathing Meditation",
        "content_type": "AUDIO",
        "read_time": "10 Min Session",
        "description": "10-minute mindfulness session to calm morning anxiety and lower daily cortisol levels.",
        "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "full_content": """
        <h4>4-7-8 Deep Diaphragmatic Breathing Protocol</h4>
        <p class="text-muted">Diaphragmatic breathing stimulates the vagus nerve, initiating parasympathetic nervous system dominance to reduce physiological stress.</p>
        <ol class="small text-muted">
            <li><strong>Inhale silently</strong> through your nose for a count of 4 seconds.</li>
            <li><strong>Hold your breath</strong> comfortably for a count of 7 seconds.</li>
            <li><strong>Exhale completely</strong> through your mouth making a gentle whoosh sound for 8 seconds.</li>
            <li>Repeat the cycle 4 to 8 times daily during morning routine.</li>
        </ol>
        """
    },
    3: {
        "resource_id": 3,
        "category": "Lifestyle & Nutrition",
        "title": "Nutrition Guide for Brain Neuroplasticity in Recovery",
        "content_type": "GUIDE",
        "read_time": "7 Min Guide",
        "description": "Discover foods rich in Omega-3, Magnesium, and Zinc that accelerate neural pathway repair.",
        "full_content": """
        <h4>Nutritional Neuro-Restoration Matrix</h4>
        <p class="text-muted">Substance dependency depletes key neuro-nutrients critical for dopamine & serotonin synthesis. The following diet plan accelerates neuro-plasticity and receptor healing:</p>
        
        <table class="table table-bordered table-sm small">
            <thead class="table-primary">
                <tr><th>Nutrient</th><th>Key Benefit</th><th>Recommended Foods</th></tr>
            </thead>
            <tbody>
                <tr><td>Omega-3 Fatty Acids</td><td>Restores neuronal cell membranes</td><td>Salmon, Walnuts, Chia seeds, Flaxseed</td></tr>
                <tr><td>Magnesium & Zinc</td><td>Reduces neuronal excitotoxicity</td><td>Spinach, Pumpkin seeds, Dark chocolate</td></tr>
                <tr><td>Complex Carbs</td><td>Stabilizes blood glucose & mood</td><td>Oats, Sweet potatoes, Quinoa, Beans</td></tr>
                <tr><td>Probiotics</td><td>Gut-Brain Axis Serotonin support</td><td>Greek Yogurt, Kefir, Kimchi, Fermented foods</td></tr>
            </tbody>
        </table>
        """
    },
    4: {
        "resource_id": 4,
        "category": "Motivational",
        "title": "Overcoming Relapses: Stories of Resilience",
        "content_type": "VIDEO",
        "read_time": "12 Min Video",
        "description": "Inspirational recovery journeys shared by former rehabilitation center patients.",
        "video_url": "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "full_content": """
        <h4>Key Takeaways from Recovery Journeys</h4>
        <ul class="small text-muted">
            <li>Relapse is a clinical setback, not a personal failure—immediate re-engagement ensures rapid bounce-back.</li>
            <li>Building a reliable peer support network doubles long-term sobriety rates.</li>
            <li>Daily habit logging creates positive momentum and rewires brain reward pathways.</li>
        </ul>
        """
    }
}


@resources_bp.route("/", methods=["GET"])
def get_educational_resources():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT resource_id, category, title, content_type, description, resource_url
            FROM educational_resources
            ORDER BY resource_id ASC
        """)
        rows = cur.fetchall()
        cur.close()

        resources = []
        if rows:
            for r in rows:
                res_id = r[0]
                detail = RESOURCE_DETAILS.get(res_id, {})
                resources.append({
                    "resource_id": res_id,
                    "category": r[1],
                    "title": r[2],
                    "content_type": r[3],
                    "description": r[4],
                    "resource_url": r[5],
                    "read_time": detail.get("read_time", "5 Min"),
                    "full_content": detail.get("full_content", "<p>Full clinical guide content available.</p>"),
                    "audio_url": detail.get("audio_url", ""),
                    "video_url": detail.get("video_url", "")
                })
        else:
            # Fallback to in-memory detailed dict if table empty
            resources = list(RESOURCE_DETAILS.values())

        return jsonify({"resources": resources}), 200
    except Exception as e:
        # Fallback to static list on any DB query issue
        return jsonify({"resources": list(RESOURCE_DETAILS.values())}), 200


@resources_bp.route("/<int:resource_id>", methods=["GET"])
def get_resource_detail(resource_id):
    resource = RESOURCE_DETAILS.get(resource_id)
    if not resource:
        return jsonify({"error": "Resource not found"}), 404
    return jsonify({"resource": resource}), 200


@resources_bp.route("/", methods=["POST"])
def add_resource():
    data = request.get_json() or {}
    category = data.get("category", "General")
    title = data.get("title", "")
    content_type = data.get("content_type", "ARTICLE")
    description = data.get("description", "")
    resource_url = data.get("resource_url", "")

    try:
        cur = mysql.connection.cursor()
        query = """
            INSERT INTO educational_resources (category, title, content_type, description, resource_url)
            VALUES (%s, %s, %s, %s, %s)
        """
        cur.execute(query, (category, title, content_type, description, resource_url))
        mysql.connection.commit()
        res_id = cur.lastrowid
        cur.close()
        return jsonify({"message": "Resource created successfully", "resource_id": res_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@resources_bp.route("/<int:resource_id>", methods=["PUT"])
def update_resource(resource_id):
    data = request.get_json() or {}
    category = data.get("category", "General")
    title = data.get("title", "")
    content_type = data.get("content_type", "ARTICLE")
    description = data.get("description", "")
    resource_url = data.get("resource_url", "")

    try:
        cur = mysql.connection.cursor()
        query = """
            UPDATE educational_resources
            SET category=%s, title=%s, content_type=%s, description=%s, resource_url=%s
            WHERE resource_id=%s
        """
        cur.execute(query, (category, title, content_type, description, resource_url, resource_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Resource updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@resources_bp.route("/<int:resource_id>", methods=["DELETE"])
def delete_resource(resource_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM educational_resources WHERE resource_id=%s", (resource_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Resource deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

