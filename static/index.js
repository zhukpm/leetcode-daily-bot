"use strict";
/* global Tabulator */

function init_participants_table(participants) {
  var table = new Tabulator("#players", {
    data: participants,
    layout: "fitDataStretch",
    headerVisible:false,
    // reactiveData: true,
    // layoutColumnsOnNewData:true,
    columns:[
      {
        title:"Name",
        field:"name",
        headerSort: false,
        hozAlign:"left",
      },
      {
        title:"Rep",
        field:"reputation",
        hozAlign:"left",
        width:65,
        headerSort: false,
        formatter:function(cell, formatterParams, onRendered){
            return "⭐ " + cell.getValue(); //return the contents of the cell;
        },
      },
      {
        title:"Submissions",
        field: "submissions",
        formatter:function(cell, formatterParams, onRendered){
            //return generateCalendarHTML(cell.getValue());
            return generateMonthlyCalendarHTML(cell.getValue());
        }
      },
      
      
    ],
  });
}

var theme = localStorage.getItem('theme') ? localStorage.getItem('theme') : 'light';
document.documentElement.setAttribute('data-theme', theme);

function toggle_dark_mode() {
  theme = theme == "dark" ? "light" : "dark";
  localStorage.setItem('theme', theme);
  document.documentElement.setAttribute('data-theme', theme);
}

/* The sliceArrayByCondition function takes two parameters:
arr: the input array.
conditionFunc: a function that defines the condition for starting a new chunk.
The array is looped through, and whenever an element satisfies the condition, a new chunk is created, and the previous chunk is added to the result.

Example:
const numbers = [1, 2, 3, 10, 4, 5, 20, 6, 7];
const chunks = sliceArrayByCondition(numbers, (num) => num > 9);
result: [ [ 1, 2, 3 ], [ 10 ], [ 4, 5 ], [ 20 ], [ 6, 7 ] ]
*/
function sliceArrayByCondition(arr, conditionFunc) {
    let chunks = [];
    let currentChunk = [];

    for (let i = 0; i < arr.length; i++) {
        const element = arr[i];
        if (conditionFunc(element)) {
            if (currentChunk.length) {
                chunks.push(currentChunk);
            }
            currentChunk = [element]; // start a new chunk with the current element
        } else {
            currentChunk.push(element);
        }
    }

    if (currentChunk.length) {
        chunks.push(currentChunk); // push the last chunk if there's any
    }

    return chunks;
}

function generateMonthlyCalendarHTML(contributionData) {
  let monthly = sliceArrayByCondition(contributionData, (contribution) => contribution['text'].endsWith("-01"));
  let result = '';
  for (let contributions of monthly) {
    result += '<div class="month">' + generateCalendarHTML(contributions) + '</div>\n';
  }
  return result;
}

function getFirstWeekDayIndex(contributionData) {
  if (contributionData.length == 0) return 0
  if (contributionData[0]['text'].startsWith('Mon')) return 0;
  if (contributionData[0]['text'].startsWith('Tue')) return 1;
  if (contributionData[0]['text'].startsWith('Wed')) return 2;
  if (contributionData[0]['text'].startsWith('Thu')) return 3;
  if (contributionData[0]['text'].startsWith('Fri')) return 4;
  if (contributionData[0]['text'].startsWith('Sat')) return 5;
  if (contributionData[0]['text'].startsWith('Sun')) return 6;
  return 0;
}

function generateCalendarHTML(contributionData) {
  let calendarHTML = '';

  let firstWeekDayIndex = getFirstWeekDayIndex(contributionData);
  for (let i = 0; i < firstWeekDayIndex; ++i) {
    contributionData.unshift({'level': 0})
  }
  
  // Break the contribution data into weeks (7 days per week)
  let weekData = [];
  for (let i = 0; i < contributionData.length; i += 7) {
    weekData.push(contributionData.slice(i, i + 7));
  }
  
  

  // Build the HTML for the calendar structure
  weekData.forEach(week => {
    calendarHTML += '<div class="week">';

    week.forEach(day => {
      // Destructure to get contributions, custom text, and link
      const { level, text, url } = day;
      if (!text) {
        calendarHTML += '<div class="day level-invisible"></div>';
      } else if (!url) {
        calendarHTML += `
          <div class="day level-${level}">
            <a title="${text}">
              ${text}
            </a>
          </div>`;
      } else {
        calendarHTML += `
          <div class="day level-${level}">
            <a href="${url}" target="_blank" title="${text}">
              ${text}
            </a>
          </div>`;
      }
      
    });

    calendarHTML += '</div>';
  });

  return calendarHTML;
}
