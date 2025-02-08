local script_path = debug.getinfo(1, "S").source:sub(2)
API_DIR = script_path:gsub("/scripts/[^/]+$", "/")

local function run_python_script(path)
    path = API_DIR .. path

    vim.fn.jobstart({ "python", path }, {
        stdout_buffered = true,
        on_stdout = function(_, data)
            if data and #data > 0 then
                local content = table.concat(data, "\n")

                vim.cmd("enew")
                local buf = vim.api.nvim_get_current_buf()

                local lines = vim.split(content, "\n")
                vim.api.nvim_buf_set_lines(buf, 0, -1, false, lines)

                vim.bo.filetype = "json"
            else
                print("No output from Python script.")
            end
        end,
        on_stderr = function(_, data)
            if data and #data > 0 then
                print("Python script error: " .. table.concat(data, "\n"))
            end
        end
    })
end

local function fetch_http(url, callback)
    vim.fn.jobstart({ "curl", "-s", url }, {
        stdout_buffered = true,
        on_stdout = function(_, data)
            if data and callback then
                local json_string = table.concat(data, "\n")
                local success, response = pcall(vim.fn.json_decode, json_string)

                if success then
                    callback(response)
                else
                    print("JSON decode error: " .. json_string)
                end
            end
        end
    })
end

local function display_in_new_buffer(content)
    vim.cmd("enew")
    local buf = vim.api.nvim_get_current_buf()

    if type(content) == "table" then
        content = vim.fn.json_encode(content)
    end

    if type(content) == "string" then
        content = vim.split(content, "\n")
    end

    vim.api.nvim_buf_set_lines(buf, 0, -1, false, content)
    vim.bo.filetype = "cpp"
end

local function get_daily_problem()
    local url = "http://127.0.0.1:8000/leetcode/daily"
    fetch_http(url, function(response)
        if response and response.codeSnippets then
            local cpp_code = nil

            for _, snippet in ipairs(response.codeSnippets) do
                if snippet.langSlug == "cpp" then
                    cpp_code = snippet.code
                    break
                end
            end

            if cpp_code then
                display_in_new_buffer(cpp_code)
            else
                print("No C++ code snippet found")
                display_in_new_buffer({ "No C++ code snippet found" })
            end
        else
            print("No codeSnippets found in response")
            display_in_new_buffer({ "No codeSnippets found in response" })
        end
    end)
end

get_daily_problem()
-- run_python_script("scripts/problem_run.py")
