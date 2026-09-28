const state = { requirements: [] };
const form = document.querySelector("#requirement-form");
const formStatus = document.querySelector("#form-status");
const notice = document.querySelector("#impact-notice");
const display = (element, message, success = true) => { element.className = `small mt-3 mb-0 ${success ? "text-success" : "text-danger"}`; element.textContent = message; };
const clearForm = () => { form.reset(); form.elements.id.value = ""; form.elements.key.disabled = false; form.hidden = true; };
async function load() {
  const [requirements, relations] = await Promise.all([fetch("/api/v1/requirements").then(r => r.json()), fetch("/api/v1/relations").then(r => r.json())]);
  state.requirements = requirements;
  document.querySelector("#requirement-count").textContent = requirements.length;
  document.querySelector("#relation-count").textContent = relations.length;
  const body = document.querySelector("#requirements-body"); body.innerHTML = "";
  requirements.forEach(item => { const row = document.createElement("tr"); row.innerHTML = `<td><strong></strong></td><td></td><td></td><td><span class="badge"></span></td><td class="text-end"><button class="btn btn-sm btn-outline-primary edit">Düzenle</button> <button class="btn btn-sm btn-outline-danger remove">Sil</button></td>`; const cells = row.querySelectorAll("td"); cells[0].querySelector("strong").textContent = item.key; cells[1].textContent = item.title; cells[2].textContent = item.requirement_type; const badge = cells[3].querySelector("span"); badge.textContent = item.status; badge.className = `badge text-bg-light border status-${item.status}`; row.querySelector(".edit").onclick = () => edit(item); row.querySelector(".remove").onclick = () => remove(item); body.appendChild(row); });
}
function edit(item) { form.hidden = false; form.elements.id.value = item.id; form.elements.key.value = item.key; form.elements.key.disabled = true; form.elements.title.value = item.title; form.elements.description.value = item.description || ""; form.elements.requirement_type.value = item.requirement_type; form.elements.status.value = item.status; form.scrollIntoView({ behavior: "smooth", block: "center" }); }
async function remove(item) { if (!window.confirm(`${item.key} silinsin mi? İlişkileri ve puanları da kaldırılır.`)) return; const response = await fetch(`/api/v1/requirements/${item.id}`, { method: "DELETE" }); if (response.ok) { display(formStatus, `${item.key} silindi.`); await load(); } else display(formStatus, "Silme işlemi başarısız.", false); }
document.querySelector("#toggle-form").onclick = () => { form.hidden = !form.hidden; if (!form.hidden) form.elements.key.focus(); };
document.querySelector("#cancel-form").onclick = clearForm;
form.addEventListener("submit", async event => { event.preventDefault(); notice.hidden = true; const id = form.elements.id.value; const payload = Object.fromEntries(new FormData(form)); delete payload.id; const response = await fetch(id ? `/api/v1/requirements/${id}` : "/api/v1/requirements", { method: id ? "PATCH" : "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) }); const data = await response.json(); if (!response.ok) { display(formStatus, data.detail || "Kayıt işlemi başarısız.", false); return; } display(formStatus, id ? "Gereksinim güncellendi." : "Gereksinim kaydedildi."); clearForm(); await load(); if (id) { const impact = await fetch(`/api/v1/impact-analysis/${encodeURIComponent(data.key)}`).then(r => r.ok ? r.json() : null); if (impact?.affected_requirements.length) { notice.hidden = false; notice.textContent = `${data.key} güncellendi: ${impact.affected_requirements.length} doğrudan veya dolaylı etki kaydı bulundu (${impact.affected_requirements.map(x => x.key).join(", ")}).`; } } });
load().catch(() => display(formStatus, "Veriler yüklenemedi.", false));
