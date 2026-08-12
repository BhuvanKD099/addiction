/**
 * AddictionSense - Educational Resources & Helplines Frontend Controller
 */

let allResources = [];

document.addEventListener("DOMContentLoaded", () => {
    loadEducationalResources();
});

async function loadEducationalResources() {
    const container = document.getElementById("resourcesGrid");
    if (!container) return;

    try {
        const response = await fetch(`${API_BASE_URL}/resources/`);
        const data = await response.json();
        
        if (data.resources && data.resources.length > 0) {
            allResources = data.resources;
        } else {
            allResources = getFallbackResources();
        }
    } catch (e) {
        console.warn("Using fallback resources due to API connectivity:", e);
        allResources = getFallbackResources();
    }

    renderResources(allResources);
}

function renderResources(resources) {
    const container = document.getElementById("resourcesGrid");
    if (!container) return;

    if (resources.length === 0) {
        container.innerHTML = `
            <div class="col-12 text-center py-5">
                <i class="bi bi-journal-x display-4 text-muted"></i>
                <h5 class="mt-3 text-muted">No resources found in this category.</h5>
            </div>
        `;
        return;
    }

    let html = "";
    resources.forEach(r => {
        let badgeClass = "bg-primary";
        let iconClass = "bi-file-text-fill";
        let btnText = "Read Full Guide";
        let btnIcon = "bi-book-half";
        let cardBorder = "border-primary";

        if (r.content_type === "AUDIO") {
            badgeClass = "bg-success";
            iconClass = "bi-headphones";
            btnText = "Listen to Audio";
            btnIcon = "bi-play-circle-fill";
            cardBorder = "border-success";
        } else if (r.content_type === "GUIDE") {
            badgeClass = "bg-info text-dark";
            iconClass = "bi-journal-check";
            btnText = "View Nutrition Plan";
            btnIcon = "bi-download";
            cardBorder = "border-info";
        } else if (r.content_type === "VIDEO") {
            badgeClass = "bg-warning text-dark";
            iconClass = "bi-film";
            btnText = "Watch Video";
            btnIcon = "bi-play-btn-fill";
            cardBorder = "border-warning";
        }

        html += `
            <div class="col-md-6 col-lg-6">
                <div class="dashboard-card p-4 border-start border-4 ${cardBorder} h-100 d-flex flex-column justify-content-between">
                    <div>
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="badge ${badgeClass}">${r.content_type}</span>
                            <small class="text-muted"><i class="bi bi-clock me-1"></i>${r.read_time || '5 Min'}</small>
                        </div>
                        <h5 class="fw-bold text-navy mb-2">${r.title}</h5>
                        <p class="text-muted small mb-3">${r.description}</p>
                    </div>
                    <div class="d-flex gap-2">
                        <button class="btn btn-outline-primary btn-sm flex-fill fw-semibold" onclick="openResourceModal(${r.resource_id})">
                            <i class="bi ${btnIcon} me-1"></i> ${btnText}
                        </button>
                        <button class="btn btn-outline-danger btn-sm" title="Delete Resource" onclick="deleteResource(${r.resource_id})">
                            <i class="bi bi-trash"></i> Delete
                        </button>
                    </div>
                </div>
            </div>
        `;
    });

    container.innerHTML = html;
}

async function deleteResource(resourceId) {
    if (!confirm("Are you sure you want to delete this educational resource?")) return;

    try {
        const response = await fetch(`${API_BASE_URL}/resources/${resourceId}`, { method: "DELETE" });
        const resData = await response.json();
        alert(resData.message || "Resource deleted.");
        loadEducationalResources();
    } catch (e) {
        console.error("Error deleting resource:", e);
        allResources = allResources.filter(r => r.resource_id !== resourceId);
        renderResources(allResources);
        alert("Resource deleted.");
    }
}

function filterResources(category) {
    // Update active tab buttons
    document.querySelectorAll(".resource-tab-btn").forEach(btn => {
        btn.classList.remove("active", "btn-primary");
        btn.classList.add("btn-outline-secondary");
    });

    event.target.classList.add("active", "btn-primary");
    event.target.classList.remove("btn-outline-secondary");

    if (category === "ALL") {
        renderResources(allResources);
    } else {
        const filtered = allResources.filter(r => r.category.toLowerCase().includes(category.toLowerCase()));
        renderResources(filtered);
    }
}

function openResourceModal(resourceId) {
    const r = allResources.find(item => item.resource_id === resourceId);
    if (!r) return;

    document.getElementById("modalResTitle").innerText = r.title;
    document.getElementById("modalResCategory").innerText = r.category;
    document.getElementById("modalResType").innerText = r.content_type;
    
    const bodyContainer = document.getElementById("modalResBody");

    let mediaHeader = "";
    if (r.content_type === "AUDIO") {
        mediaHeader = `
            <div class="p-3 bg-light rounded border mb-3 text-center">
                <h6 class="fw-bold text-success mb-2"><i class="bi bi-headphones me-2"></i>Guided Recovery Audio Player</h6>
                <audio controls class="w-100">
                    <source src="${r.audio_url || 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            </div>
        `;
    } else if (r.content_type === "VIDEO") {
        mediaHeader = `
            <div class="p-3 bg-dark rounded mb-3 text-center text-white">
                <h6 class="fw-bold text-warning mb-2"><i class="bi bi-film me-2"></i>Motivational Video Story</h6>
                <div class="ratio ratio-16x9">
                    <iframe src="${r.video_url || 'https://www.youtube.com/embed/dQw4w9WgXcQ'}" title="Recovery Video" allowfullscreen></iframe>
                </div>
            </div>
        `;
    }

    bodyContainer.innerHTML = mediaHeader + (r.full_content || `<p class="text-muted">${r.description}</p>`);

    const modal = new bootstrap.Modal(document.getElementById("resourceViewModal"));
    modal.show();
}

function getFallbackResources() {
    return [
        {
            resource_id: 1,
            category: "Coping Techniques",
            title: "10 Grounding Exercises for Acute Cravings",
            content_type: "ARTICLE",
            read_time: "5 Min Read",
            description: "Learn the 5-4-3-2-1 sensory technique to navigate intense craving waves without yielding.",
            full_content: `
                <h4>The 5-4-3-2-1 Coping & Grounding Technique</h4>
                <p class="text-muted">When a sudden craving occurs, your nervous system triggers heightened distress. Grounding exercises redirect neurological focus back to the physical environment, lowering acute anxiety within 90 seconds.</p>
                <div class="p-3 bg-light rounded border mb-2"><strong>5 Things You Can SEE:</strong> Look around your room. Name 5 specific items out loud.</div>
                <div class="p-3 bg-light rounded border mb-2"><strong>4 Things You Can TOUCH:</strong> Feel the texture of your shirt, cold water on your hands, or solid ground.</div>
                <div class="p-3 bg-light rounded border mb-2"><strong>3 Things You Can HEAR:</strong> Listen closely for 3 distinct background sounds.</div>
                <div class="p-3 bg-light rounded border mb-2"><strong>2 Things You Can SMELL:</strong> Inhale deeply and notice subtle ambient scents.</div>
                <div class="p-3 bg-light rounded border mb-2"><strong>1 Thing You Can TASTE:</strong> Take a sip of cool mint tea or lemon water.</div>
            `
        },
        {
            resource_id: 2,
            category: "Mindfulness & Meditation",
            title: "Guided Morning Recovery Breathing Meditation",
            content_type: "AUDIO",
            read_time: "10 Min Session",
            description: "10-minute mindfulness session to calm morning anxiety and lower daily cortisol levels.",
            audio_url: "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
            full_content: `
                <h4>4-7-8 Deep Breathing Protocol</h4>
                <p class="text-muted">Diaphragmatic breathing stimulates the vagus nerve, initiating parasympathetic nervous system dominance to reduce physiological stress.</p>
                <ol class="small text-muted">
                    <li>Inhale silently through your nose for 4 seconds.</li>
                    <li>Hold your breath comfortably for 7 seconds.</li>
                    <li>Exhale completely through your mouth for 8 seconds.</li>
                    <li>Repeat cycle 4 times during morning routine.</li>
                </ol>
            `
        },
        {
            resource_id: 3,
            category: "Lifestyle & Nutrition",
            title: "Nutrition Guide for Brain Neuroplasticity in Recovery",
            content_type: "GUIDE",
            read_time: "7 Min Guide",
            description: "Discover foods rich in Omega-3, Magnesium, and Zinc that accelerate neural pathway repair.",
            full_content: `
                <h4>Nutritional Neuro-Restoration Matrix</h4>
                <p class="text-muted">Substance dependency depletes key neuro-nutrients critical for dopamine & serotonin synthesis. The following diet plan accelerates neuro-plasticity:</p>
                <table class="table table-bordered table-sm small">
                    <thead class="table-primary">
                        <tr><th>Nutrient</th><th>Key Benefit</th><th>Recommended Foods</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Omega-3 Fatty Acids</td><td>Restores neuronal cell membranes</td><td>Salmon, Walnuts, Chia seeds</td></tr>
                        <tr><td>Magnesium & Zinc</td><td>Reduces neuronal excitotoxicity</td><td>Spinach, Pumpkin seeds</td></tr>
                        <tr><td>Complex Carbs</td><td>Stabilizes blood glucose & mood</td><td>Oats, Sweet potatoes, Quinoa</td></tr>
                        <tr><td>Probiotics</td><td>Gut-Brain Serotonin support</td><td>Greek Yogurt, Kefir, Kimchi</td></tr>
                    </tbody>
                </table>
            `
        },
        {
            resource_id: 4,
            category: "Motivational",
            title: "Overcoming Relapses: Stories of Resilience",
            content_type: "VIDEO",
            read_time: "12 Min Video",
            description: "Inspirational recovery journeys shared by former rehabilitation center patients.",
            video_url: "https://www.youtube.com/embed/dQw4w9WgXcQ",
            full_content: `
                <h4>Key Takeaways from Recovery Journeys</h4>
                <ul class="small text-muted">
                    <li>Relapse is a clinical setback, not a personal failure—immediate re-engagement ensures rapid bounce-back.</li>
                    <li>Building a reliable peer support network doubles long-term sobriety rates.</li>
                    <li>Daily habit logging creates positive momentum and rewires brain reward pathways.</li>
                </ul>
            `
        }
    ];
}
