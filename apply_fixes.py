#!/usr/bin/env python3
"""
Apply all identified fixes to the BNV Cover Maker HTML file.
Reads the source, applies targeted string replacements, writes fixed output.
"""

import re

SRC = '/root/.claude/uploads/7880cd32-cb71-4ae4-9863-56b3a0ab8641/287d5903-Finalv30.html'
DST = '/home/user/my-codex-test-/fixed_BNV_Cover_Maker.html'

with open(SRC, 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)
fixes_applied = []

# ==============================================================
# FIX 1: Remove duplicate .pm-bottom-tabs CSS rule (second one at ~line 544)
# The second definition uses hardcoded #fff and height:64px, overriding the
# theme-aware first definition. Remove the duplicate block.
# ==============================================================
OLD1 = """/* --- BOTTOM TABS (CANVA STYLE) --- */
.pm-bottom-tabs {
  background: #fff !important;
  border-top: 1px solid #f1f5f9 !important;
  padding: 0 !important;
  display: flex !important;
  justify-content: space-around !important;
  align-items: center !important;
  flex-shrink: 0 !important;
  height: 64px !important;
  box-shadow: 0 -1px 4px rgba(0,0,0,.04) !important;
}"""
if OLD1 in html:
    html = html.replace(OLD1, '/* .pm-bottom-tabs duplicate removed - using themed definition above */', 1)
    fixes_applied.append('Fix 1: Removed duplicate .pm-bottom-tabs CSS (kept themed version)')
else:
    fixes_applied.append('Fix 1 SKIPPED: .pm-bottom-tabs duplicate not found (may have different spacing)')

# ==============================================================
# FIX 2: Global button CSS reset with !important breaks all styled buttons.
# Remove the destructive background:transparent and border:none !important overrides.
# Keep only appearance and cursor which are safe resets.
# ==============================================================
OLD2 = """/* Button standardization */
button {
  -webkit-appearance: none !important;
  -moz-appearance: none !important;
  appearance: none !important;
  border: none !important;
  background: transparent !important;
  cursor: pointer !important;
  padding: 0 !important;
  font-family: inherit !important;
}"""
NEW2 = """/* Button standardization - FIXED: removed border/background !important overrides
   that were breaking .btn-primary, .btn-outline, .btn-seg etc */
button {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  cursor: pointer;
  font-family: inherit;
}"""
if OLD2 in html:
    html = html.replace(OLD2, NEW2, 1)
    fixes_applied.append('Fix 2: Fixed global button reset - removed destructive border/background !important overrides')
else:
    fixes_applied.append('Fix 2 SKIPPED: global button reset block not found with exact whitespace')

# ==============================================================
# FIX 3: Consolidate duplicate input/select/textarea font-size rules.
# There are 3 blocks setting font-size:16px or font-size:max(16px,1em).
# Keep only the first (at ~line 3591) and remove the later duplicates.
# ==============================================================
OLD3a = """\ninput, select, textarea {
  font-size: max(16px, 1em) !important;
}"""
# This appears twice - remove both occurrences after the first (the one at 3591 is a single block)
count_before = html.count(OLD3a)
if count_before >= 2:
    # Remove all but keep the first occurrence
    first_idx = html.find(OLD3a)
    # Remove from second occurrence onwards
    rest = html[first_idx + len(OLD3a):]
    rest_fixed = rest.replace(OLD3a, '\n/* duplicate input font-size rule removed */', 1)
    html = html[:first_idx + len(OLD3a)] + rest_fixed
    fixes_applied.append(f'Fix 3: Removed duplicate input/select/textarea font-size rules ({count_before} found, kept first)')
else:
    fixes_applied.append(f'Fix 3 SKIPPED: found {count_before} occurrences of duplicate font-size rule')

# ==============================================================
# FIX 4: Duplicate id="themeBtn" - rename the second occurrence to themeBtn2
# and update updateThemeBtn() to update both buttons.
# Line 4918 = mobile design card (keep as themeBtn)
# Line 5225 = desktop sidebar (rename to themeBtn2)
# ==============================================================
# The two occurrences are identical except position.
# We need to rename only the SECOND occurrence.
TBTN_PATTERN = 'id="themeBtn" onclick="toggleTheme()"'
first_pos = html.find(TBTN_PATTERN)
second_pos = html.find(TBTN_PATTERN, first_pos + 1)
if first_pos >= 0 and second_pos >= 0:
    html = html[:second_pos] + 'id="themeBtn2" onclick="toggleTheme()"' + html[second_pos + len(TBTN_PATTERN):]
    fixes_applied.append('Fix 4: Renamed second themeBtn to themeBtn2 (desktop sidebar)')
else:
    fixes_applied.append(f'Fix 4 SKIPPED: found {1 if first_pos >= 0 else 0} themeBtn occurrences')

# ==============================================================
# FIX 5: Update updateThemeBtn() to update both themeBtn and themeBtn2
# ==============================================================
OLD5 = """function updateThemeBtn(){
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const btn = document.getElementById('themeBtn');
  if(btn) btn.textContent = isDark ? '\\u2600\\uFE0F' : '\\uD83C\\uDF19';
}"""
NEW5 = """function updateThemeBtn(){
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const emoji = isDark ? '\\u2600\\uFE0F' : '\\uD83C\\uDF19';
  const btn = document.getElementById('themeBtn');
  if(btn) btn.textContent = emoji;
  const btn2 = document.getElementById('themeBtn2');
  if(btn2) btn2.textContent = emoji;
}"""
if OLD5 in html:
    html = html.replace(OLD5, NEW5, 1)
    fixes_applied.append('Fix 5: Updated updateThemeBtn() to update both themeBtn and themeBtn2')
else:
    fixes_applied.append('Fix 5 SKIPPED: updateThemeBtn function not found with exact text')

# ==============================================================
# FIX 6: Unify dark mode systems - toggleDark() and toggleTheme() use
# different localStorage keys and variables. Make toggleDark() also
# call updateThemeBtn() so all theme buttons stay in sync.
# ==============================================================
OLD6 = """function toggleDark(){
  _darkMode = !_darkMode;
  document.documentElement.setAttribute('data-theme', _darkMode ? 'dark' : '');
  var btn = E('dark-btn');
  if(btn) btn.textContent = _darkMode ? '\\u2600\\ufe0f' : '\\uD83C\\uDF19';
  try{ localStorage.setItem('bnv_dark', _darkMode ? '1' : ''); }catch(e){}
}"""
NEW6 = """function toggleDark(){
  _darkMode = !_darkMode;
  document.documentElement.setAttribute('data-theme', _darkMode ? 'dark' : '');
  var btn = E('dark-btn');
  if(btn) btn.textContent = _darkMode ? '\\u2600\\ufe0f' : '\\uD83C\\uDF19';
  // Sync bnv-theme key and themeBtn buttons
  try{ localStorage.setItem('bnv_dark', _darkMode ? '1' : ''); }catch(e){}
  try{ localStorage.setItem('bnv-theme', _darkMode ? 'dark' : 'light'); }catch(e){}
  if(typeof updateThemeBtn==='function') updateThemeBtn();
}"""
if OLD6 in html:
    html = html.replace(OLD6, NEW6, 1)
    fixes_applied.append('Fix 6: Unified toggleDark() to sync bnv-theme key and themeBtn buttons')
else:
    fixes_applied.append('Fix 6 SKIPPED: toggleDark function not found with exact text')

# ==============================================================
# FIX 7: Unify initDark() to also check bnv-theme localStorage key
# so dark mode persists correctly regardless of which toggle was used.
# ==============================================================
OLD7 = """function initDark(){
  try{
    var saved = localStorage.getItem('bnv_dark');
    if(saved === '1'){ _darkMode = true; document.documentElement.setAttribute('data-theme','dark'); var btn=E('dark-btn');if(btn)btn.textContent='\\u2600\\ufe0f'; }
  }catch(e){}
}"""
NEW7 = """function initDark(){
  try{
    var savedDark = localStorage.getItem('bnv_dark');
    var savedTheme = localStorage.getItem('bnv-theme');
    var isDark = savedDark === '1' || savedTheme === 'dark';
    if(isDark){
      _darkMode = true;
      document.documentElement.setAttribute('data-theme','dark');
      var btn=E('dark-btn');if(btn)btn.textContent='\\u2600\\ufe0f';
    }
  }catch(e){}
}"""
if OLD7 in html:
    html = html.replace(OLD7, NEW7, 1)
    fixes_applied.append('Fix 7: Updated initDark() to check both bnv_dark and bnv-theme localStorage keys')
else:
    fixes_applied.append('Fix 7 SKIPPED: initDark function not found with exact text')

# ==============================================================
# FIX 8: toggleTheme() loadTheme() - also sync _darkMode variable
# so the header dark-btn stays consistent with themeBtn.
# ==============================================================
OLD8 = """function toggleTheme(){
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  document.documentElement.setAttribute('data-theme', isDark ? '' : 'dark');
  localStorage.setItem('bnv-theme', isDark ? 'light' : 'dark');
  updateThemeBtn();
}
function loadTheme(){
  const theme = localStorage.getItem('bnv-theme') || 'light';
  if(theme === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
  updateThemeBtn();
}"""
NEW8 = """function toggleTheme(){
  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
  const newDark = !isDark;
  document.documentElement.setAttribute('data-theme', newDark ? 'dark' : '');
  try{ localStorage.setItem('bnv-theme', newDark ? 'dark' : 'light'); }catch(e){}
  try{ localStorage.setItem('bnv_dark', newDark ? '1' : ''); }catch(e){}
  // Sync _darkMode variable so toggleDark/dark-btn stays in sync
  if(typeof _darkMode !== 'undefined') { /* jshint ignore:line */ }
  _darkMode = newDark;
  var headerBtn = document.getElementById('dark-btn');
  if(headerBtn) headerBtn.textContent = newDark ? '\\u2600\\ufe0f' : '\\uD83C\\uDF19';
  updateThemeBtn();
}
function loadTheme(){
  const theme = localStorage.getItem('bnv-theme') || localStorage.getItem('bnv_dark') === '1' ? 'dark' : 'light';
  const isDark = theme === 'dark';
  if(isDark) document.documentElement.setAttribute('data-theme', 'dark');
  _darkMode = isDark;
  var headerBtn = document.getElementById('dark-btn');
  if(headerBtn) headerBtn.textContent = isDark ? '\\u2600\\ufe0f' : '\\uD83C\\uDF19';
  updateThemeBtn();
}"""
if OLD8 in html:
    html = html.replace(OLD8, NEW8, 1)
    fixes_applied.append('Fix 8: Fixed toggleTheme()/loadTheme() to sync _darkMode variable and dark-btn header button')
else:
    fixes_applied.append('Fix 8 SKIPPED: toggleTheme/loadTheme block not found')

# ==============================================================
# FIX 9: Remove duplicate toggleSectionColors() function definition
# The second one at ~line 9139 replaces the first at ~line 8719.
# The second has slightly different logic (uses || for two IDs).
# Keep the second (more comprehensive) version, remove the first.
# ==============================================================
OLD9 = """function toggleSectionColors(){
  var body=E('sc-body');
  var arrow=E('sc-arrow');
  if(!body)return;
  var open=body.style.display!=='none';
  body.style.display=open?'none':'block';
  if(arrow)arrow.style.transform=open?'rotate(0)':'rotate(180deg)';
}
window.toggleSectionColors=toggleSectionColors;"""
NEW9 = """/* toggleSectionColors moved below - consolidated into single function */
// window.toggleSectionColors defined below"""
if OLD9 in html:
    html = html.replace(OLD9, NEW9, 1)
    fixes_applied.append('Fix 9: Removed first duplicate toggleSectionColors() - kept comprehensive second version')
else:
    fixes_applied.append('Fix 9 SKIPPED: first toggleSectionColors not found with exact text')

# ==============================================================
# FIX 10: Remove the stray "loadTheme();" calls that appear as
# standalone calls (not inside functions) - they cause loadTheme to
# run before DOM is ready (lines ~8326, 9082, 9278, 9421, 9460).
# These are inside IIFEs alongside event listener setup, which is fine,
# but the pattern "loadTheme();document.addEventListener('DOMContentLoaded'..."
# is problematic because loadTheme() runs immediately (before DOM ready).
# Fix: Move loadTheme calls to inside the DOMContentLoaded handlers.
# ==============================================================

# Fix the IIFE in the ResizeObserver block (line ~9082)
OLD10a = """  loadTheme();document.addEventListener('DOMContentLoaded', function(){
    var pb = document.querySelector('.preview-body');
    if(pb) ro.observe(pb);
  });"""
NEW10a = """  document.addEventListener('DOMContentLoaded', function(){
    if(typeof loadTheme==='function') loadTheme();
    var pb = document.querySelector('.preview-body');
    if(pb) ro.observe(pb);
  });"""
if OLD10a in html:
    html = html.replace(OLD10a, NEW10a, 1)
    fixes_applied.append('Fix 10a: Moved loadTheme() inside DOMContentLoaded in ResizeObserver IIFE')
else:
    fixes_applied.append('Fix 10a SKIPPED: ResizeObserver IIFE loadTheme pattern not found')

# Fix the stray loadTheme() before document.addEventListener('click'...) at ~line 9278
OLD10b = """loadTheme();document.addEventListener('click',function(e){
  if(!e.target.closest('#topic-search-wrap')){
    var res=E('topic-search-results');if(res)res.style.display='none';
  }
});"""
NEW10b = """document.addEventListener('click',function(e){
  if(!e.target.closest('#topic-search-wrap')){
    var res=E('topic-search-results');if(res)res.style.display='none';
  }
});"""
if OLD10b in html:
    html = html.replace(OLD10b, NEW10b, 1)
    fixes_applied.append('Fix 10b: Removed stray loadTheme() before click listener for topic-search')
else:
    fixes_applied.append('Fix 10b SKIPPED: topic-search loadTheme pattern not found')

# Fix the stray loadTheme() in the main DOMContentLoaded block at ~line 9421
OLD10c = """loadTheme();document.addEventListener('DOMContentLoaded',function(){
  // V13-FIXED: Each call wrapped to prevent one failure breaking all
  function _safe(name, fn){"""
NEW10c = """document.addEventListener('DOMContentLoaded',function(){
  // Load theme at DOM ready
  if(typeof loadTheme==='function') loadTheme();
  // V13-FIXED: Each call wrapped to prevent one failure breaking all
  function _safe(name, fn){"""
if OLD10c in html:
    html = html.replace(OLD10c, NEW10c, 1)
    fixes_applied.append('Fix 10c: Moved loadTheme() inside main DOMContentLoaded handler')
else:
    fixes_applied.append('Fix 10c SKIPPED: main DOMContentLoaded loadTheme pattern not found')

# Fix the stray loadTheme() before click ac-wrap listener at ~line 9460
OLD10d = """  loadTheme();document.addEventListener('click',function(e){if(!e.target.closest('.ac-wrap')){const l=E('ac-list');if(l)l.classList.remove('open');}});"""
NEW10d = """  document.addEventListener('click',function(e){if(!e.target.closest('.ac-wrap')){const l=E('ac-list');if(l)l.classList.remove('open');}});"""
if OLD10d in html:
    html = html.replace(OLD10d, NEW10d, 1)
    fixes_applied.append('Fix 10d: Removed stray loadTheme() before ac-wrap click listener')
else:
    fixes_applied.append('Fix 10d SKIPPED: ac-wrap loadTheme pattern not found')

# Fix the stray loadTheme() in touch swipe IIFE at ~line 8326
OLD10e = """  loadTheme();document.addEventListener('DOMContentLoaded',function(){
    var cmpStage=E('pm-compare-stage');"""
NEW10e = """  document.addEventListener('DOMContentLoaded',function(){
    var cmpStage=E('pm-compare-stage');"""
if OLD10e in html:
    html = html.replace(OLD10e, NEW10e, 1)
    fixes_applied.append('Fix 10e: Removed stray loadTheme() in touch swipe IIFE')
else:
    fixes_applied.append('Fix 10e SKIPPED: touch swipe loadTheme pattern not found')

# ==============================================================
# FIX 11: BED-EPC template broken string concatenation
# Lines 7879-7887 have JS strings that accidentally produce string
# literal text instead of HTML. The ternary operators return
# quoted strings like '+"<div ..."' instead of actual HTML strings.
# ==============================================================
OLD11 = """    +(guideDes?'+"<div style=\\"font-size:"+infoFz+"pt;font-weight:600;color:"+cBlue+\\";\\">"+guideDes+"</div>"':'')
    +(guide2N?'+"<div style=\\"font-size:"+nameFz2+"pt;font-weight:700;color:"+cBlue+";margin-top:4px\\">"+guide2N+"</div>"':'')
    +(guide2D?'+"<div style=\\"font-size:"+infoFz+"pt;font-weight:600;color:"+cBlue+\\";\\">"+guide2D+"</div>"':'')
    +(guideDep?'+"<div style=\\"font-size:"+infoFz+"pt;font-weight:600;color:"+cBlue+\\";\\">"+guideDep+"</div>"':'')"""
NEW11 = """    +(guideDes?'<div style="font-size:'+infoFz+'pt;font-weight:600;color:'+cBlue+'">'+guideDes+'</div>':'')
    +(guide2N?'<div style="font-size:'+nameFz2+'pt;font-weight:700;color:'+cBlue+';margin-top:4px">'+guide2N+'</div>':'')
    +(guide2D?'<div style="font-size:'+infoFz+'pt;font-weight:600;color:'+cBlue+'">'+guide2D+'</div>':'')
    +(guideDep?'<div style="font-size:'+infoFz+'pt;font-weight:600;color:'+cBlue+'">'+guideDep+'</div>':'')"""
if OLD11 in html:
    html = html.replace(OLD11, NEW11, 1)
    fixes_applied.append('Fix 11: Fixed bed-epc template broken string concatenation (guide details now render as HTML)')
else:
    fixes_applied.append('Fix 11 SKIPPED: bed-epc broken string pattern not found')

# Similarly fix the rollN line in the BED-EPC student section
OLD11b = """    +(rollN?'+"<div style=\\"font-size:"+infoFz+"pt;font-weight:600;color:"+cBlue+\\";\\">Roll No. : - "+rollN+"</div>"':'')"""
NEW11b = """    +(rollN?'<div style="font-size:'+infoFz+'pt;font-weight:600;color:'+cBlue+'">Roll No. : - '+rollN+'</div>':'')"""
if OLD11b in html:
    html = html.replace(OLD11b, NEW11b, 1)
    fixes_applied.append('Fix 11b: Fixed bed-epc template rollN broken string concatenation')
else:
    fixes_applied.append('Fix 11b SKIPPED: bed-epc rollN broken string pattern not found')

# ==============================================================
# FIX 12: loadTheme() in the save/load section (line ~7329) calls
# toast('No theme saved') which requires DOM to be ready.
# The function itself is fine - used at right time. No change needed.

# FIX 13: toggleTheme loadTheme function - the loadTheme() call inside
# a save/load function that depends on toast() is fine because it's
# only called at user interaction time. No change needed here.

# FIX 14: The _var var _currentTpl is declared twice (lines 7353 and at the
# global section ~line 6097). The second declaration shadows the first.
# Remove the duplicate var declaration.
# ==============================================================
OLD14 = """var _pmPage='fp';
var _pmView='compare';  // default view
var _pmCmpIdx=0;        // compare template pair index
var _pmTouchX=0;
var _currentTpl='standard';
var _borderStyle='';
var _logoPos='center';
var _topicStyle='box'; // Track current template key"""
NEW14 = """var _pmPage='fp';
var _pmView='compare';  // default view
var _pmCmpIdx=0;        // compare template pair index
var _pmTouchX=0;
// Note: _currentTpl, _borderStyle, _logoPos, _topicStyle are declared globally above
// Re-initializing here for modal section defaults (these are the same variables)
if(typeof _currentTpl==='undefined') var _currentTpl='standard';
if(typeof _borderStyle==='undefined') var _borderStyle='';
if(typeof _logoPos==='undefined') var _logoPos='center';
if(typeof _topicStyle==='undefined') var _topicStyle='box';"""
if OLD14 in html:
    html = html.replace(OLD14, NEW14, 1)
    fixes_applied.append('Fix 14: Fixed duplicate _currentTpl/_borderStyle/_logoPos/_topicStyle variable declarations')
else:
    fixes_applied.append('Fix 14 SKIPPED: duplicate variable block not found')

# ==============================================================
# FIX 15: The pmApplyTemplate() function has a double loop updating
# active state on .pm-tpl-btn. First loop does useless work, second
# is the correct one. Remove the first useless loop.
# ==============================================================
OLD15 = """  // Update modal template buttons
  document.querySelectorAll('.pm-tpl-btn').forEach(function(b){
    var on=b.textContent.trim()===TEMPLATES.find(function(t){return t.k===k;})?.l;
    b.classList.toggle('on',b.onclick&&b.onclick.toString().includes("'"+k+"'"));
  });
  document.querySelectorAll('.pm-tpl-btn').forEach(function(b){
    b.classList.remove('on');
    if(b.getAttribute('onclick')&&b.getAttribute('onclick').includes("'"+k+"'"))b.classList.add('on');
  });"""
NEW15 = """  // Update modal template buttons
  document.querySelectorAll('.pm-tpl-btn').forEach(function(b){
    b.classList.remove('on');
    if(b.getAttribute('onclick')&&b.getAttribute('onclick').includes("'"+k+"'"))b.classList.add('on');
  });"""
if OLD15 in html:
    html = html.replace(OLD15, NEW15, 1)
    fixes_applied.append('Fix 15: Removed redundant first loop in pmApplyTemplate() button state update')
else:
    fixes_applied.append('Fix 15 SKIPPED: pmApplyTemplate double loop not found')

# ==============================================================
# FIX 16: The V22 restoreFormData() conflicts with the existing loadData()
# function which uses SCHEMA to restore data. Having two separate restoration
# systems can cause conflicts. Add a guard to prevent V22 from restoring
# if loadData has already run (i.e. if SK localStorage key is set).
# ==============================================================
OLD16 = """  function restoreFormData(){
    try {
      var raw = localStorage.getItem('bnv_form_data');
      if (!raw) return;
      var data = JSON.parse(raw);
      Object.keys(data).forEach(function(id){
        var input = document.getElementById(id);
        if (input && !input.value && data[id]){
          input.value = data[id];
        }
      });"""
NEW16 = """  function restoreFormData(){
    try {
      // Guard: don't restore if loadData() already handled it (SK key present)
      if (localStorage.getItem('bnv_cv3') || localStorage.getItem('bnv_cv3_h')) return;
      var raw = localStorage.getItem('bnv_form_data');
      if (!raw) return;
      var data = JSON.parse(raw);
      Object.keys(data).forEach(function(id){
        var input = document.getElementById(id);
        if (input && !input.value && data[id]){
          input.value = data[id];
        }
      });"""
if OLD16 in html:
    html = html.replace(OLD16, NEW16, 1)
    fixes_applied.append('Fix 16: Added guard in restoreFormData() to prevent conflict with loadData()')
else:
    fixes_applied.append('Fix 16 SKIPPED: restoreFormData function not found with exact text')

# ==============================================================
# FIX 17: The modal keyboard listener at line ~9926 checks for
# '.prev-modal.show' but the modal uses class 'open' not 'show'.
# Fix the selector.
# ==============================================================
OLD17 = """    var modal=document.querySelector('.prev-modal.show');
    if(!modal) return;
    var cur=window._pmPage||'fp';
    var idx=PAGE_ORDER.indexOf(cur);
    if(e.key==='ArrowLeft'&&idx>0){
      e.preventDefault();
      var p=PAGE_ORDER[idx-1];
      switchPage(p,document.querySelector('.pm-ptab[onclick*="'+p+'"]'));
    } else if(e.key==='ArrowRight'&&idx<PAGE_ORDER.length-1){
      e.preventDefault();
      var p2=PAGE_ORDER[idx+1];
      switchPage(p2,document.querySelector('.pm-ptab[onclick*="'+p2+'"]'));
    } else if(e.key==='Escape'){
      try{ if(typeof closeModal==='function') closeModal(); }catch(err){}
    }"""
NEW17 = """    var modal=document.querySelector('.prev-modal.open');
    if(!modal) return;
    var cur=window._pmPage||'fp';
    var idx=PAGE_ORDER.indexOf(cur);
    if(e.key==='ArrowLeft'&&idx>0){
      e.preventDefault();
      var p=PAGE_ORDER[idx-1];
      switchPage(p,document.querySelector('.pm-ptab[onclick*="'+p+'"]'));
    } else if(e.key==='ArrowRight'&&idx<PAGE_ORDER.length-1){
      e.preventDefault();
      var p2=PAGE_ORDER[idx+1];
      switchPage(p2,document.querySelector('.pm-ptab[onclick*="'+p2+'"]'));
    } else if(e.key==='Escape'){
      try{ if(typeof closeModal==='function') closeModal(); }catch(err){}
    }"""
if OLD17 in html:
    html = html.replace(OLD17, NEW17, 1)
    fixes_applied.append('Fix 17: Fixed keyboard listener to use .prev-modal.open instead of .prev-modal.show')
else:
    fixes_applied.append('Fix 17 SKIPPED: keyboard listener .prev-modal.show pattern not found')

# ==============================================================
# FIX 18: The V18 keyboard shortcut block also uses '.prev-modal.open'
# correctly (line ~10406) - no change needed there.
# But the v10 bindKeys() uses '.prev-modal.show' (line ~9927) - already fixed above.

# FIX 19: pmApplyFont() uses broken regex escaping for font name matching.
# The function: b.getAttribute('onclick').includes(fv.replace(/'/g,"\\\\\\'"))
# This tries to match font names but the escaping is wrong.
# Fix to use a simpler data-attribute matching approach.
# ==============================================================
OLD19 = """function pmApplyFont(fv){
  setFont(fv);
  document.querySelectorAll('.pm-font-btn').forEach(function(b){b.classList.toggle('on',b.getAttribute('onclick')&&b.getAttribute('onclick').includes(fv.replace(/'/g,"\\\\\\'")));});
  pmRefreshMini();
}"""
NEW19 = """function pmApplyFont(fv){
  setFont(fv);
  document.querySelectorAll('.pm-font-btn').forEach(function(b){
    // Use data-font attribute or font-family style for matching
    var bFont = b.style.fontFamily || '';
    b.classList.toggle('on', bFont.trim() === fv.trim() ||
      (b.getAttribute('onclick') && b.getAttribute('onclick').includes(fv.substring(0,12))));
  });
  pmRefreshMini();
}"""
if OLD19 in html:
    html = html.replace(OLD19, NEW19, 1)
    fixes_applied.append('Fix 19: Fixed pmApplyFont() broken regex escaping for font name matching')
else:
    fixes_applied.append('Fix 19 SKIPPED: pmApplyFont with broken regex not found')

# ==============================================================
# FIX 20: The buildDesktopSidebar() at line ~8991 uses local variable
# 'cc' which shadows the outer 'cc()' color function in pmBuildFpHtml.
# Rename the local variable to avoid confusion.
# ==============================================================
OLD20 = """  // Sync color input
  var cc=E('custom-col-desk');if(cc)cc.value=_col;"""
NEW20 = """  // Sync color input
  var ccEl=E('custom-col-desk');if(ccEl)ccEl.value=_col;"""
if OLD20 in html:
    html = html.replace(OLD20, NEW20, 1)
    fixes_applied.append('Fix 20: Renamed conflicting local var cc to ccEl in buildDesktopSidebar()')
else:
    fixes_applied.append('Fix 20 SKIPPED: local var cc pattern not found')

# ==============================================================
# FIX 21: The sleep() function at line 8474 is called as:
#   doDownload();sleep(700).then(()=>{doWAOpen();showInstr();});
# This is fine. But sleep() is called in generateAll() as:
#   switchPage(pages[i]);await sleep(400);
# sleep() is defined as a Promise function - OK.
# No fix needed.

# FIX 22: The pmBuildModalPage() function sets _pmPage but the
# pmSwitchPage() function also sets _page (the global form page var).
# When switching pages in the modal, _page (global) gets modified which
# can affect alt page rendering. The restored save of savedPage is correct.
# No change needed.

# FIX 23: In the V22 phase, restoreLastTemplate() has a comment saying
# "Don't auto-click" but it loads the template name from localStorage
# without actually applying it. This means the template won't be restored
# on refresh. Fix: properly restore last template.
# Actually this is intentional (to avoid side effects). Leave as is.

# FIX 24: The scrollbar fix - V25 EMBED sends height via setInterval every
# 1000ms which is wasteful and can conflict with resize. The ResizeObserver
# is better. But this is a performance issue not a bug. Leave as is.

# FIX 25: The topic buildTopicUI() at line 9684 checks:
#   if(!wrap || document.getElementById('topic-dropdown')) return;
# This prevents re-building the dropdown if it already exists, even after
# the element might have been removed from DOM. This is fine.

# FIX 26: Duplicate loadTheme() in the touch swipe IIFE (line 8326) -
# already fixed in Fix 10e above.

# Final summary
print(f"\\nFixes applied: {len(fixes_applied)}")
print(f"Original file size: {original_len:,} chars")
print(f"Fixed file size: {len(html):,} chars")
print(f"\\nFix results:")
for f in fixes_applied:
    status = "OK" if "SKIPPED" not in f else "SKIP"
    print(f"  [{status}] {f}")

with open(DST, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"\\nFixed file written to: {DST}")
