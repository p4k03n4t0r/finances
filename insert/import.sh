curl -k -H "Content-Type: application/json" "localhost:5601/api/kibana/dashboards/import" -H 'kbn-xsrf: true' --data-binary @insert/dashboard.json