workflow "Format on Push" {
  on = "push"
  resolves = ["Lint"]
}

action "Lint" {
  uses = "lgeiger/black-action@master"
  args = ". --check"
}
